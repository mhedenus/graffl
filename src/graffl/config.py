import logging
import uuid

logger = logging.getLogger(__name__)


class GrafflConfig:
    def __init__(self):
        self.uri_prefix = f"https://www.hedenus.de/graffl/{uuid.uuid1()}/"
        self.dictionary = {

            ":": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "=": "http://www.w3.org/1999/02/22-rdf-syntax-ns#value",
            "value": "http://www.w3.org/1999/02/22-rdf-syntax-ns#value",

            "Property": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",
            "*": "http://www.w3.org/1999/02/22-rdf-syntax-ns#li",
            "Alt": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt",
            "Bag": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag",
            "Seq": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq",

            "Class": "http://www.w3.org/2000/01/rdf-schema#Class",
            "Datatype": "http://www.w3.org/2000/01/rdf-schema#Datatype",
            "label": "http://www.w3.org/2000/01/rdf-schema#label",
            "comment": "http://www.w3.org/2000/01/rdf-schema#comment",
            ";": "http://www.w3.org/2000/01/rdf-schema#comment",
            "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
            "subPropertyOf": "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
            "seeAlso": "http://www.w3.org/2000/01/rdf-schema#seeAlso",
            "isDefinedBy": "http://www.w3.org/2000/01/rdf-schema#isDefinedBy",

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


CONFIG = GrafflConfig()
