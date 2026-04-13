import logging
import os
import re
from enum import Enum
from pathlib import Path
from urllib.parse import quote

from lark import Lark, Token
from lark.visitors import Interpreter
from rdflib import URIRef, Literal, Graph, RDFS, RDF, BNode
from rdflib.parser import Parser

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

    def __str__(self):
        return f"{self.type}: {self.value}"

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


class GrafflASTInterpreter(Interpreter):

    def __init__(self, sink):
        self.sink = sink

        self.subjects_seen = set()
        self.current_group_graph = None
        self.current_subjects_in_group_graph = None

        self.current_subject = None
        self.current_predicate = None
        self.current_predicate_type = None
        self.current_subject_stack = None
        self.current_language = None

        self.current_uri_prefix = CONFIG.uri_prefix
        self.dictionary = dict(CONFIG.dictionary)
        self.uri_properties = {URIRef(i) for i in CONFIG.uri_properties}

        self.group_contains = URIRef(CONFIG.group_contains)
        self.group_type = URIRef(CONFIG.group_type)

    def _get_raw_value(self, node):
        if not getattr(node, 'children', None):
            return str(node)
        token = node.children[0]
        return token.value if isinstance(token, Token) else str(token)

    def _make_uri(self, word):
        val = word.value
        if not val:
            raise ValueError("empty word value")

        if val in self.dictionary:
            return URIRef(self.dictionary[val])
        elif word.type == WordType.URI:
            return URIRef(val)
        else:
            encoded_val = quote(val, safe="/:=#")
            return URIRef(f"{self.current_uri_prefix}{encoded_val}")

    def _make_uri_predicate(self, word):
        if re.match(r"\d+\.", word.value):
            num = word.value[:-1]
            return URIRef(f"http://www.w3.org/1999/02/22-rdf-syntax-ns#_{num}")
        else:
            return self._make_uri(word)

    def _remember_subject(self, subject, word):
        if not subject in self.subjects_seen:
            if not (word.type == WordType.URI or word.type == WordType.NODEREF):
                self.add_triple((subject, RDFS.label, Literal(word.value)))
            self.subjects_seen.add(subject)

    # ==========================================
    # Interpreter-Methoden (Top-Down Logik)
    # ==========================================

    def directive(self, tree):
        if len(tree.children) >= 2:
            token1 = Word(self._get_raw_value(tree.children[0]).lower())
            token2 = Word(self._get_raw_value(tree.children[1]))

            if len(tree.children) == 2 and token1.value == "prefix" and token2.type == WordType.URI:
                self.current_uri_prefix = token2.value
                logger.debug(f"uri_prefix set: {self.current_uri_prefix}")

            elif len(tree.children) == 3 and token2.value == "=":
                token3 = Word(self._get_raw_value(tree.children[2]))
                if token3.type == WordType.URI:
                    self.dictionary[token1.value] = token3.value

            elif len(tree.children) == 3 and token2.value == ":":
                token3 = Word(self._get_raw_value(tree.children[2]))

                if token3.value == "URI":
                    property_uri = self._make_uri(token1)
                    self.uri_properties.add(property_uri)
                #TODO typing of predicates



    def block(self, tree):
        self.current_subject = None
        self.current_predicate = None
        self.current_predicate_type = None
        self.visit_children(tree)

    def subject(self, tree):
        word = Word(self._get_raw_value(tree))
        subject = self._make_uri(word)
        self._remember_subject(subject, word)

        self.current_subject_stack = []
        self.current_subject_stack.append(subject)

        if self.current_group_graph:
            if not subject in self.current_subjects_in_group_graph:
                self.add_triple((self.current_group_graph, self.group_contains, subject))
                self.current_subjects_in_group_graph.add(subject)

        self.current_subject = subject

    def blank_node_begin(self, tree):
        bnode = BNode()
        self.add_triple((self.current_subject, self.current_predicate, bnode))
        self.current_subject_stack.append(bnode)
        self.current_subject = bnode

        if self.current_group_graph:
            if not bnode in self.current_subjects_in_group_graph:
                self.add_triple((self.current_group_graph, self.group_contains, bnode))
                self.current_subjects_in_group_graph.add(bnode)

    def blank_node_end(self, tree):
        self.current_subject_stack.pop()
        self.current_subject = self.current_subject_stack[-1]

    def predicate_property(self, tree):
        word = Word(self._get_raw_value(tree))
        self.current_predicate = self._make_uri_predicate(word)
        self.current_predicate_type = PredicateType.PROPERTY
        if len(tree.children) == 2 and tree.children[1].type == "LANG_ISO_CODE":
            self.current_language = tree.children[1].value[1:]

    def predicate_relation(self, tree):
        word = Word(self._get_raw_value(tree.children[0]))
        self.current_predicate = self._make_uri_predicate(word)
        self.current_predicate_type = PredicateType.RELATION

    def object(self, tree):
        word = Word(self._get_raw_value(tree))

        if self.current_predicate_type == PredicateType.PROPERTY:
            # propert is Literal except:
            #  - property is URI
            #  - listed in uri_properties
            if word.type == WordType.URI or (self.current_predicate in self.uri_properties):
                obj = self._make_uri(word)
            else:
                if self.current_language:
                    obj = Literal(word.value, lang=self.current_language)
                else:
                    obj = Literal(word.value)
        elif self.current_predicate_type == PredicateType.RELATION:
            # relation asserts an URI
            obj = self._make_uri(word)
        else:
            raise Exception(f"illegal state: {self.current_predicate_type}")

        self.current_language = None  # reset in any case

        if self.current_subject and self.current_predicate and obj:
            self.add_triple((self.current_subject, self.current_predicate, obj))

    def group_graph(self, tree):
        word = Word(self._get_raw_value(tree.children[0]))
        graph_name_str = word.value
        logger.debug(f"group graph begin: {graph_name_str}")

        self.current_group_graph = self._make_uri(word)
        self.add_triple((self.current_group_graph, RDF.type, self.group_type))
        self._remember_subject(self.current_group_graph, word)

        self.current_subjects_in_group_graph = set()

        self.visit_children(tree)

        self.current_group_graph = None
        self.current_subjects_in_group_graph = None

        logger.debug(f"group graph end: {graph_name_str}")

    def add_triple(self, triple):
        logger.debug(f"{triple[0]} {triple[1]} {triple[2]}")
        self.sink.add(triple)


class GrafflParser(Parser):
    """
    Custom Parser for RDF-format 'graffl'.
    """

    def __init__(self):
        super().__init__()

        with open(GRAMMAR_FILE, 'r', encoding='utf-8') as f:
            grammar_text = f.read()

        self.lark_parser = Lark(grammar_text, start='start', parser='lalr')  # lalr is fast but restricts grammar

    def parse(self, source, sink, **kwargs):
        stream = source.getCharacterStream()
        if stream is None:
            raise ValueError("No character stream available.")

        content = stream.read()

        tree = self.lark_parser.parse(content)

        logger.debug(f"--- AST STRUCTURE ---\n{tree.pretty()}\n---------------------")

        interpreter = GrafflASTInterpreter(sink)
        interpreter.visit(tree)


def parse(input):
    data = None
    if isinstance(input, Path):
        with open(input, 'r', encoding='utf-8') as f:
            data = f.read()
    if isinstance(input, str):
        data = input

    g = Graph()

    if data == "":
        return g

    if data:
        g.parse(data=data, format="graffl", plugin_parsers={"graffl": GrafflParser})
        return g
    else:
        raise ValueError(f"Unsupported input: {type(input)}")
