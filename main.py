import logging

from rdflib import Graph

import graffl.parser

log_level = logging.DEBUG
logging.basicConfig(
    level=log_level,
    format="%(levelname)s: %(message)s"
)

g = Graph()

test_graffl_data = """
@ prefix  urn:exmaple.org#

    Michael : x
        "hat Geburtstag" 08.02.1974
        email michael@hedenus.de
        homepage https://www.hedenus.de#/~mhedenus/?q1=x1&q2=x2()#1
        mag -> Doris
    
    Doris
    

"""


g.parse(data=test_graffl_data, format="graffl")

for subj, pred, obj in g:
    print(f"Subjekt: {subj}, Prädikat: {pred}, Objekt: {obj}")
