import logging
from rdflib.namespace import XSD

logger = logging.getLogger(__name__)


class GrafflConfig:
    def __init__(self):
        self.base_uri = "https://www.hedenus.de/graffl/"

        self.dictionary = {
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
            "rdfsClass": "http://www.w3.org/2000/01/rdf-schema#Class",
            "Datatype": "http://www.w3.org/2000/01/rdf-schema#Datatype",
            "label": "http://www.w3.org/2000/01/rdf-schema#label",
            "comment": "http://www.w3.org/2000/01/rdf-schema#comment",
            ";": "http://www.w3.org/2000/01/rdf-schema#comment",
            "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
            "subPropertyOf": "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
            "seeAlso": "http://www.w3.org/2000/01/rdf-schema#seeAlso",
            "isDefinedBy": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",

            # --- OWL Core (NEU) ---
            "Class": "http://www.w3.org/2002/07/owl#Class",
            "Ontology": "http://www.w3.org/2002/07/owl#Ontology",
            "Restriction": "http://www.w3.org/2002/07/owl#Restriction",
            "onProperty": "http://www.w3.org/2002/07/owl#onProperty",
            "someValuesFrom": "http://www.w3.org/2002/07/owl#someValuesFrom",
            "allValuesFrom": "http://www.w3.org/2002/07/owl#allValuesFrom",
            "hasValue": "http://www.w3.org/2002/07/owl#hasValue",
            "intersectionOf": "http://www.w3.org/2002/07/owl#intersectionOf",
            "unionOf": "http://www.w3.org/2002/07/owl#unionOf",
            "oneOf": "http://www.w3.org/2002/07/owl#oneOf",
            "equivalentClass": "http://www.w3.org/2002/07/owl#equivalentClass",
            "disjointWith": "http://www.w3.org/2002/07/owl#disjointWith",
            "ObjectProperty": "http://www.w3.org/2002/07/owl#ObjectProperty",
            "DatatypeProperty": "http://www.w3.org/2002/07/owl#DatatypeProperty",
            "NamedIndividual": "http://www.w3.org/2002/07/owl#NamedIndividual",

            # --- rdf2graphml ---
            "color": "https://www.hedenus.de/rdf2graphml/color",
            "shape": "https://www.hedenus.de/rdf2graphml/shape",
            "icon": "https://www.hedenus.de/rdf2graphml/icon",
            "lineType": "https://www.hedenus.de/rdf2graphml/lineType",
            "targetArrow": "https://www.hedenus.de/rdf2graphml/targetArrow"
        }

        self.uri_properties = {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "http://www.w3.org/2000/01/rdf-schema#subClassOf",
            "http://www.w3.org/2002/07/owl#allValuesFrom",
            "http://www.w3.org/2002/07/owl#annotatedProperty",
            "http://www.w3.org/2002/07/owl#annotatedSource",
            "http://www.w3.org/2002/07/owl#annotatedTarget",
            "http://www.w3.org/2002/07/owl#assertionProperty",
            "http://www.w3.org/2002/07/owl#backwardCompatibleWith",
            "http://www.w3.org/2002/07/owl#bottomDataProperty",
            "http://www.w3.org/2002/07/owl#bottomObjectProperty",
            "http://www.w3.org/2002/07/owl#cardinality",
            "http://www.w3.org/2002/07/owl#complementOf",
            "http://www.w3.org/2002/07/owl#datatypeComplementOf",
            "http://www.w3.org/2002/07/owl#deprecated",
            "http://www.w3.org/2002/07/owl#differentFrom",
            "http://www.w3.org/2002/07/owl#disjointUnionOf",
            "http://www.w3.org/2002/07/owl#disjointWith",
            "http://www.w3.org/2002/07/owl#distinctMembers",
            "http://www.w3.org/2002/07/owl#equivalentClass",
            "http://www.w3.org/2002/07/owl#equivalentProperty",
            "http://www.w3.org/2002/07/owl#hasKey",
            "http://www.w3.org/2002/07/owl#hasSelf",
            "http://www.w3.org/2002/07/owl#hasValue",
            "http://www.w3.org/2002/07/owl#imports",
            "http://www.w3.org/2002/07/owl#incompatibleWith",
            "http://www.w3.org/2002/07/owl#intersectionOf",
            "http://www.w3.org/2002/07/owl#inverseOf",
            "http://www.w3.org/2002/07/owl#maxCardinality",
            "http://www.w3.org/2002/07/owl#maxQualifiedCardinality",
            "http://www.w3.org/2002/07/owl#members",
            "http://www.w3.org/2002/07/owl#minCardinality",
            "http://www.w3.org/2002/07/owl#minQualifiedCardinality",
            "http://www.w3.org/2002/07/owl#onClass",
            "http://www.w3.org/2002/07/owl#onDataRange",
            "http://www.w3.org/2002/07/owl#onDatatype",
            "http://www.w3.org/2002/07/owl#onProperties",
            "http://www.w3.org/2002/07/owl#onProperty",
            "http://www.w3.org/2002/07/owl#oneOf",
            "http://www.w3.org/2002/07/owl#priorVersion",
            "http://www.w3.org/2002/07/owl#propertyChainAxiom",
            "http://www.w3.org/2002/07/owl#propertyDisjointWith",
            "http://www.w3.org/2002/07/owl#qualifiedCardinality",
            "http://www.w3.org/2002/07/owl#sameAs",
            "http://www.w3.org/2002/07/owl#someValuesFrom",
            "http://www.w3.org/2002/07/owl#sourceIndividual",
            "http://www.w3.org/2002/07/owl#targetIndividual",
            "http://www.w3.org/2002/07/owl#targetValue",
            "http://www.w3.org/2002/07/owl#topDataProperty",
            "http://www.w3.org/2002/07/owl#topObjectProperty",
            "http://www.w3.org/2002/07/owl#unionOf",
            "http://www.w3.org/2002/07/owl#versionIRI",
            "http://www.w3.org/2002/07/owl#versionInfo",
            "http://www.w3.org/2002/07/owl#withRestrictions",
        }

        self.xsd_types = {
            "string": XSD.string,
            "boolean": XSD.boolean,
            "integer": XSD.integer,
            "decimal": XSD.decimal,
            "float": XSD.float,
            "double": XSD.double,
            "dateTime": XSD.dateTime,
            "time": XSD.time,
            "date": XSD.date,
            "anyURI": XSD.anyURI,
        }

        self.group_contains = "https://www.hedenus.de/graffl/contains"
        self.group_type = "https://www.hedenus.de/graffl/Group"


CONFIG = GrafflConfig()
