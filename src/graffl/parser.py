import os
from rdflib import URIRef, Literal
from rdflib.parser import Parser
from lark import Lark, Transformer

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'graffl.lark')

class GrafflToRDFTransformer(Transformer):
    """
    Diese Klasse wandelt die von Lark erkannten Knoten direkt in rdflib-Objekte um.
    Die Methoden heißen exakt so wie die Regeln in der .lark Datei.
    """

    def __init__(self, sink):
        # Wir übergeben den Ziel-Graphen, um direkt Tripel speichern zu können
        self.sink = sink

    # --- Terminals umwandeln ---
    def URI(self, token):
        # Entfernt die spitzen Klammern: <http://example.org> -> http://example.org
        return URIRef(token.value[1:-1])

    def STRING(self, token):
        # Entfernt die Anführungszeichen: "Wert" -> Wert
        return Literal(token.value[1:-1])

    def KEYWORD(self, token):
        # Beispiel: Wir definieren einen eigenen Namensraum für unsere Keywords
        return URIRef(f"http://graffl.org/vocab/{token.value.lower()}")

    # --- Baumknoten (Rules) auflösen ---
    def subject(self, children):
        return children[0]

    def predicate(self, children):
        return children[0]

    def object(self, children):
        return children[0]

    def statement(self, children):
        # Ein 'statement' besteht laut Grammatik aus subject, predicate, object.
        # Lark übergibt uns diese in der 'children' Liste.
        subj, pred, obj = children[0], children[1], children[2]

        # Füge das fertige Tripel dem Graphen hinzu!
        #self.sink.add((subj, pred, obj))

        # Rückgabewert ist hier egal, da wir es direkt in den sink speichern
        return None


class GrafflParser(Parser):
    """
    Ein benutzerdefinierter Parser für das RDF-Format 'graffl'.
    """

    def __init__(self):
        super().__init__()

        # Grammatik einmalig beim Laden der Klasse kompilieren (für bessere Performance)
        with open(GRAMMAR_FILE, 'r', encoding='utf-8') as f:
            grammar_text = f.read()

        # Wir nutzen den schnellen 'lalr' Parser
        self.lark_parser = Lark(grammar_text, start='start', parser='lalr')

    def parse(self, source, sink, **kwargs):
        """
        Liest 'graffl' Daten aus einer Quelle und schreibt die Tripel in den Zielgraphen (sink).
        """
        stream = source.getCharacterStream()
        if stream is None:
            raise ValueError("No character stream available.")

        # Lese den gesamten Text aus dem Stream
        content = stream.read()

        # 1. Lark baut den Syntaxbaum (AST)
        tree = self.lark_parser.parse(content)

        print("--- AST STRUKTUR ---")
        print(tree.pretty())
        print("--------------------")

        # 2. Transformer instanziieren und den Sink übergeben
       # transformer = GrafflToRDFTransformer(sink)

        # 3. Baum durchlaufen lassen. Der Transformer ruft automatisch 
        #    sink.add() auf, wenn er ein 'statement' findet.
        #transformer.transform(tree)