import logging

logger = logging.getLogger(__name__)


class GrafflConfig:
    def __init__(self):
        self.uri_prefix = "https://www.hedenus.de/graffl/"
        self.dictionary = {

            ":": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "a": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "Property": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property",

            "Class": "http://www.w3.org/2002/07/owl#Class",
            "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",

            "color": "https://www.hedenus.de/rdf2graphml/color",
            "icon": "https://www.hedenus.de/rdf2graphml/icon"
        }
        self.uri_properties = {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        }
        self.group_contains = "https://www.hedenus.de/graffl/contains"
        self.group_type = "https://www.hedenus.de/graffl/Group"


CONFIG = GrafflConfig()
