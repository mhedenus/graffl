import os
import logging
from urllib.parse import quote
from rdflib import URIRef, Literal, Graph, RDFS, RDF
from rdflib.parser import Parser
from lark import Lark, Token
from lark.visitors import Interpreter

# Importiere unser Konfigurationsobjekt
from .config import CONFIG

logger = logging.getLogger(__name__)
GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'graffl.lark')


class GrafflASTInterpreter(Interpreter):
    """
    Durchläuft den abstrakten Syntaxbaum (AST) streng Top-Down.
    Dies erlaubt uns, Gültigkeitsbereiche (Scopes) wie innere Graphen
    zu betreten und wieder sauber zu verlassen.
    """

    def __init__(self, sink):
        self.sink = sink

        # --- Zustandsvariablen (State) ---
        self.entities = {}
        self.current_inner_graph = None
        self.current_entities_in_inner_graph = None

        self.current_subject = None
        self.current_predicate = None
        self.current_predicate_type = None  # 'property' oder 'relation'

        self.current_uri_prefix = CONFIG.uri_prefix
        self.dictionary = dict(CONFIG.dictionary)
        self.uri_properties = {URIRef(i) for i in CONFIG.uri_properties}

        self.group_contains = URIRef(CONFIG.group_contains)
        self.group_type = URIRef(CONFIG.group_type)


    # ==========================================
    # Hilfsmethoden für RDF-Knoten
    # ==========================================

    def _is_uri(self, val):
        return val.startswith('<') and val.endswith('>')

    def _get_raw_value(self, node):
        if not getattr(node, 'children', None):
            return str(node)
        token = node.children[0]
        return token.value if isinstance(token, Token) else str(token)

    def _clean_string(self, val):
        if val.startswith('"""') and val.endswith('"""'):
            return val[3:-3]
        elif val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val

    def _make_uri(self, val):
        if self._is_uri(val):
            return URIRef(val[1:-1])

        clean_val = self._clean_string(val)

        if clean_val in self.dictionary:
            return URIRef(self.dictionary[clean_val])
        else:
            # Präfix anhängen und URL-kodieren (safe="/:=#" schützt gewollte Trenner)
            encoded_val = quote(clean_val, safe="/:=#")
            return URIRef(f"{self.current_uri_prefix}{encoded_val}")

    # ==========================================
    # Interpreter-Methoden (Top-Down Logik)
    # ==========================================

    def directive(self, tree):
        """Fängt Direktiven wie '@ prefix ...' ab und überschreibt den Zustand."""
        if len(tree.children) >= 2:
            command = self._get_raw_value(tree.children[0]).lower()

            if command == "prefix":
                new_prefix = self._get_raw_value(tree.children[1])

                # Klammern oder Anführungszeichen aufräumen
                if new_prefix.startswith('<') and new_prefix.endswith('>'):
                    new_prefix = new_prefix[1:-1]
                elif new_prefix.startswith('"') and new_prefix.endswith('"'):
                    new_prefix = new_prefix[1:-1]

                self.current_uri_prefix = new_prefix
                logger.debug(f"URI prefix overridden by script: {self.current_uri_prefix}")

    def inner_graph(self, tree):

        graph_name_str = self._clean_string(self._get_raw_value(tree.children[0]))
        logger.debug(f"Entering inner graph: {graph_name_str}")

        self.current_inner_graph = self._make_uri(graph_name_str)
        self.add_triple((self.current_inner_graph, RDF.type, self.group_type))
        self.add_triple((self.current_inner_graph, RDFS.label, Literal(graph_name_str)))
        self.current_entities_in_inner_graph = set()

        self.visit_children(tree)

        self.current_inner_graph = None
        self.current_entities_in_inner_graph = None

        logger.debug(f"Leaving inner graph: {graph_name_str}")


    def block(self, tree):
        self.current_subject = None
        self.current_predicate = None
        self.current_predicate_type = None
        self.visit_children(tree)

    def subject(self, tree):
        val = self._get_raw_value(tree)
        subject = self._make_uri(val)

        if not val in self.entities:
            self.add_triple((subject, RDFS.label, Literal(self._clean_string(val))))
            self.entities[val] = self.current_subject

        if self.current_inner_graph:
            if not subject in self.current_entities_in_inner_graph:
                self.add_triple((self.current_inner_graph, self.group_contains, subject))

        self.current_subject = subject

    def predicate_property(self, tree):
        val = self._get_raw_value(tree)
        self.current_predicate = self._make_uri(val)
        self.current_predicate_type = 'property'

    def predicate_relation(self, tree):
        val = self._get_raw_value(tree.children[0])
        self.current_predicate = self._make_uri(val)
        self.current_predicate_type = 'relation'

    def object(self, tree):
        val = self._get_raw_value(tree)

        if self.current_predicate_type == 'property':
            # Property erzwingt immer ein Literal, ausser wenn ausdrücklich URI oder Spezial
            if self._is_uri(val) or (self.current_predicate in self.uri_properties):
                obj = self._make_uri(val)
            else:
                clean_val = self._clean_string(val)
                obj = Literal(clean_val)

        elif self.current_predicate_type == 'relation':
            # Relation erzwingt immer eine URI
            obj = self._make_uri(val)

        else:
            return

        if self.current_subject and self.current_predicate and obj:
            self.add_triple((self.current_subject, self.current_predicate, obj))

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

        # Wir nutzen den schnellen 'lalr' Parser
        self.lark_parser = Lark(grammar_text, start='start', parser='lalr')

    def parse(self, source, sink, **kwargs):
        stream = source.getCharacterStream()
        if stream is None:
            raise ValueError("No character stream available.")

        content = stream.read()

        tree = self.lark_parser.parse(content)

        logger.debug(f"--- AST STRUCTURE ---\n{tree.pretty()}\n---------------------")

        interpreter = GrafflASTInterpreter(sink)
        interpreter.visit(tree)