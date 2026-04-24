import logging

from rdflib import OWL
from rdflib.namespace import RDF, RDFS, XSD, FOAF, SKOS, DCTERMS

logger = logging.getLogger(__name__)


class GrafflConfig:
    def __init__(self):
        self.base_uri = "https://www.hedenus.de/graffl/"

        self.dictionary = {
            # --- Standard Namespace Prefixes ---
            "rdf": str(RDF),
            "rdfs": str(RDFS),
            "xsd": str(XSD),
            "owl": str(OWL),
            "sh": "http://www.w3.org/ns/shacl#",
            "foaf": str(FOAF),
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": str(DCTERMS),
            "skos": str(SKOS),
            "schema": "https://schema.org/",
            "rdf2graphml": "https://www.hedenus.de/rdf2graphml/",

            # --- RDF Core ---
            ":": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "=": "http://www.w3.org/1999/02/22-rdf-syntax-ns#value",
            "value": "http://www.w3.org/1999/02/22-rdf-syntax-ns#value",
            "Property": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",
            "*": "http://www.w3.org/1999/02/22-rdf-syntax-ns#li",
            "Alt": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt",
            "Bag": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag",
            "Seq": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq",

            # --- RDFS Core ---
            "label": "http://www.w3.org/2000/01/rdf-schema#label",
            "comment": "http://www.w3.org/2000/01/rdf-schema#comment",
            ";": "http://www.w3.org/2000/01/rdf-schema#comment",
            "seeAlso": "http://www.w3.org/2000/01/rdf-schema#seeAlso",

            # --- rdf2graphml ---
            "color": "https://www.hedenus.de/rdf2graphml/color",
            "shape": "https://www.hedenus.de/rdf2graphml/shape",
            "icon": "https://www.hedenus.de/rdf2graphml/icon",
            "lineType": "https://www.hedenus.de/rdf2graphml/lineType",
            "targetArrow": "https://www.hedenus.de/rdf2graphml/targetArrow"
        }

        self.uri_properties = {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        }

        self.group_contains = "https://www.hedenus.de/graffl/contains"
        self.group_type = "https://www.hedenus.de/graffl/Group"

        self.xsd_types = {
            "anyURI": XSD.anyURI,
            "base64Binary": XSD.base64Binary,
            "boolean": XSD.boolean,
            "byte": XSD.byte,
            "date": XSD.date,
            "dateTime": XSD.dateTime,
            "dateTimeStamp": XSD.dateTimeStamp,
            "dayTimeDuration": XSD.dayTimeDuration,
            "decimal": XSD.decimal,
            "double": XSD.double,
            "duration": XSD.duration,
            "float": XSD.float,
            "gDay": XSD.gDay,
            "gMonth": XSD.gMonth,
            "gMonthDay": XSD.gMonthDay,
            "gYear": XSD.gYear,
            "gYearMonth": XSD.gYearMonth,
            "hexBinary": XSD.hexBinary,
            "int": XSD.int,
            "integer": XSD.integer,
            "long": XSD.long,
            "negativeInteger": XSD.negativeInteger,
            "nonNegativeInteger": XSD.nonNegativeInteger,
            "nonPositiveInteger": XSD.nonPositiveInteger,
            "positiveInteger": XSD.positiveInteger,
            "short": XSD.short,
            "string": XSD.string,
            "time": XSD.time,
            "unsignedByte": XSD.unsignedByte,
            "unsignedInt": XSD.unsignedInt,
            "unsignedLong": XSD.unsignedLong,
            "unsignedShort": XSD.unsignedShort,
            "yearMonthDuration": XSD.yearMonthDuration
        }


CONFIG = GrafflConfig()
