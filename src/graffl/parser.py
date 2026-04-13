import logging
import os
import re
import uuid
from enum import Enum
from pathlib import Path
from urllib.parse import quote
from contextlib import contextmanager

from lark import Lark, Token
from lark.visitors import Interpreter
from lark.exceptions import UnexpectedInput, LarkError

from rdflib import URIRef, Literal, Graph, RDFS, RDF, BNode
from rdflib.parser import Parser
from rdflib.collection import Collection

from .config import CONFIG

logger = logging.getLogger(__name__)
GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'graffl.lark')


class WordType(Enum):
    PLAIN = 0
    URI = 1
    NODEREF = 2
    ML_STRING = 3
    STRING = 4


class PredicateType(Enum):
    PROPERTY = 1
    RELATION = 2


class Word:
    def __init__(self, raw_value):
        if self._is_uri(raw_value):
            self.type = WordType.URI
            self.value = self._strip(raw_value)
        elif self._is_noderef(raw_value):
            self.type = WordType.NODEREF
            self.value = self._strip(raw_value)
        elif self._is_ml_string(raw_value):
            self.type = WordType.ML_STRING
            self.value = self._strip_mls_quotes(raw_value)
        elif self._is_string(raw_value):
            self.type = WordType.STRING
            self.value = self._strip(raw_value)
        else:
            self.type = WordType.PLAIN
            self.value = raw_value

    def _is_uri(self, val):
        return val.startswith('<') and val.endswith('>')

    def _is_noderef(self, val):
        return val.startswith('(') and val.endswith(')')

    def _is_ml_string(self, val):
        return val.startswith('"""') and val.endswith('"""')

    def _is_string(self, val):
        return val.startswith('"') and val.endswith('"')

    def _strip(self, val):
        return val[1:-1]

    def _strip_mls_quotes(self, val):
        return val[3:-3]

    def __str__(self):
        return f"{self.type}: {self.value}"


class GrafflASTInterpreter(Interpreter):
    def __init__(self, sink):
        self.sink = sink
        self.subjects_seen = set()

        # Zustandsvariablen
        self.current_subject = None
        self.current_predicate = None
        self.current_predicate_type = None
        self.current_subject_stack = []
        self.current_language = None
        self.current_datatype = None

        # Listen-Management
        self.current_list_items_stack = []
        self.route_to_list = False

        # Group Graph Management
        self.current_group_graph = None
        self.current_subjects_in_group_graph = None

        self.current_uri_prefix = f"{CONFIG.base_uri}{uuid.uuid1()}/"

        self.dictionary = dict(CONFIG.dictionary)
        self.uri_properties = {URIRef(i) for i in CONFIG.uri_properties}

        # Datatypes
        self.xsd_types = dict(getattr(CONFIG, 'xsd_types', {}))

        self.group_contains = URIRef(CONFIG.group_contains)
        self.group_type = URIRef(CONFIG.group_type)

    # ==========================================
    # Context Managers (State Machine)
    # ==========================================

    @contextmanager
    def subject_context(self, new_subject):
        """Wechselt das Subjekt und deaktiviert das Routing in Listen für den Scope."""
        self.current_subject_stack.append(new_subject)
        self.current_subject = new_subject
        old_route = self.route_to_list
        self.route_to_list = False
        try:
            yield
        finally:
            self.route_to_list = old_route
            self.current_subject_stack.pop()
            self.current_subject = self.current_subject_stack[-1] if self.current_subject_stack else None

    @contextmanager
    def list_item_context(self):
        """Aktiviert das Routing von Objekten in die aktuelle Liste."""
        old_route = self.route_to_list
        self.route_to_list = True
        try:
            yield
        finally:
            self.route_to_list = old_route

    @contextmanager
    def group_graph_context(self, group_uri):
        """Kapselt den Scope eines Group Graphs."""
        old_group = self.current_group_graph
        old_subjects = self.current_subjects_in_group_graph
        self.current_group_graph = group_uri
        self.current_subjects_in_group_graph = set()
        try:
            yield
        finally:
            self.current_group_graph = old_group
            self.current_subjects_in_group_graph = old_subjects

    # ==========================================
    # Hilfsmethoden & URI Generierung
    # ==========================================

    def _get_raw_value(self, node):
        if not getattr(node, 'children', None): return str(node)
        token = node.children[0]
        return token.value if isinstance(token, Token) else str(token)

    def _make_uri(self, word):
        val = word.value
        if val in self.dictionary: return URIRef(self.dictionary[val])
        if word.type == WordType.URI: return URIRef(val)
        return URIRef(f"{self.current_uri_prefix}{quote(val, safe='/:=#')}")

    def _make_uri_predicate(self, word):
        if re.match(r"\d+\.", word.value):
            return URIRef(f"http://www.w3.org/1999/02/22-rdf-syntax-ns#_{word.value[:-1]}")
        return self._make_uri(word)

    def _remember_subject(self, subject, word):
        if subject not in self.subjects_seen:
            if word.type not in (WordType.URI, WordType.NODEREF):
                self.sink.add((subject, RDFS.label, Literal(word.value)))
            self.subjects_seen.add(subject)

    # ==========================================
    # Interpreter Methoden
    # ==========================================

    def directive(self, tree):
        if len(tree.children) >= 2:
            t1 = Word(self._get_raw_value(tree.children[0]).lower())
            t2 = Word(self._get_raw_value(tree.children[1]))
            if t1.value == "prefix" and t2.type == WordType.URI:
                self.current_uri_prefix = t2.value
            elif len(tree.children) == 3 and tree.children[1] == "=":
                self.dictionary[t1.value] = Word(self._get_raw_value(tree.children[2])).value
            elif len(tree.children) == 3 and tree.children[1] == ":":
                if self._get_raw_value(tree.children[2]) == "URI":
                    self.uri_properties.add(self._make_uri(t1))

    def block(self, tree):
        self.current_subject = None
        self.visit_children(tree)

    def subject(self, tree):
        word = Word(self._get_raw_value(tree))
        subject = self._make_uri(word)
        self._remember_subject(subject, word)
        self.current_subject_stack = [subject]
        self.current_subject = subject
        if self.current_group_graph and subject not in self.current_subjects_in_group_graph:
            self.sink.add((self.current_group_graph, self.group_contains, subject))
            self.current_subjects_in_group_graph.add(subject)

    def predicate_property(self, tree):
        word = Word(self._get_raw_value(tree.children[0]))
        self.current_predicate = self._make_uri_predicate(word)
        self.current_predicate_type = PredicateType.PROPERTY

        self.current_language = None
        self.current_datatype = None

        if len(tree.children) == 2:
            tag_value = tree.children[1].value[1:]  # Das '@' am Anfang abschneiden

            if tag_value in self.xsd_types:
                self.current_datatype = self.xsd_types[tag_value]
            else:
                self.current_language = tag_value

    def predicate_relation(self, tree):
        word = Word(self._get_raw_value(tree.children[0]))
        self.current_predicate = self._make_uri_predicate(word)
        self.current_predicate_type = PredicateType.RELATION

    def object(self, tree):
        word = Word(self._get_raw_value(tree))
        if self.current_predicate_type == PredicateType.PROPERTY:
            if word.type == WordType.URI or (self.current_predicate in self.uri_properties):
                obj = self._make_uri(word)
            else:
                obj = Literal(word.value, lang=self.current_language, datatype=self.current_datatype)
        else:
            obj = self._make_uri(word)

        self.current_language = None
        self.current_datatype = None

        if self.route_to_list:
            self.current_list_items_stack[-1].append(obj)
        elif self.current_subject and self.current_predicate:
            self.sink.add((self.current_subject, self.current_predicate, obj))

    def blank_node(self, tree):
        bnode = BNode()
        if self.route_to_list:
            self.current_list_items_stack[-1].append(bnode)
        elif self.current_subject and self.current_predicate:
            self.sink.add((self.current_subject, self.current_predicate, bnode))

        if self.current_group_graph and bnode not in self.current_subjects_in_group_graph:
            self.sink.add((self.current_group_graph, self.group_contains, bnode))
            self.current_subjects_in_group_graph.add(bnode)

        with self.subject_context(bnode):
            self.visit_children(tree)

    def rdf_list(self, tree):
        head = BNode()
        if self.route_to_list:
            self.current_list_items_stack[-1].append(head)
        elif self.current_subject and self.current_predicate:
            self.sink.add((self.current_subject, self.current_predicate, head))

        self.current_list_items_stack.append([])
        self.visit_children(tree)
        items = self.current_list_items_stack.pop()
        Collection(self.sink, head, items)

    def list_item(self, tree):
        with self.list_item_context():
            self.visit_children(tree)

    def group_graph(self, tree):
        word = Word(self._get_raw_value(tree.children[0]))
        group_uri = self._make_uri(word)
        self.sink.add((group_uri, RDF.type, self.group_type))
        self._remember_subject(group_uri, word)
        with self.group_graph_context(group_uri):
            self.visit_children(tree)


class GrafflParser(Parser):
    def __init__(self):
        super().__init__()
        with open(GRAMMAR_FILE, 'r', encoding='utf-8') as f:
            grammar_text = f.read()
        self.lark_parser = Lark(grammar_text, start='start', parser='lalr')

    def parse(self, source, sink, **kwargs):
        content = source.getCharacterStream().read()
        tree = self.lark_parser.parse(content)
        GrafflASTInterpreter(sink).visit(tree)


def parse(input, graph=None):
    data = input.read_text(encoding='utf-8') if isinstance(input, Path) else input
    g = graph if graph is not None else Graph()
    if not data: return g
    try:
        g.parse(data=data, format="graffl", plugin_parsers={"graffl": GrafflParser})
        return g
    except UnexpectedInput as e:
        raise ValueError(f"Syntax error (Line {e.line}, Col {e.column}):\n{e.get_context(data)}") from None
    except LarkError as e:
        raise ValueError(f"Parser error: {str(e)}") from None