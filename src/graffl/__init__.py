import rdflib
from rdflib.parser import Parser

from .parser import GrafflParser

rdflib.plugin.register(
    'graffl',  # Format-Name
    Parser,  # Plugin-Typ
    'graffl.parser',
    'GrafflParser'
)
