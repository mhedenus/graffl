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
@ prefix  http://example.org/data/

---- Graph1 ----

    Michael : Person
        "hatGeburtstag" 08.02.1974
        email michael@hedenus.de
        homepage https://www.hedenus.de#/~mhedenus/?q1=x1&q2=x2()#1
        mag -> Doris
    
    Doris

-----   

"""


g.parse(data=test_graffl_data, format="graffl")

output = g.serialize(format="turtle")
print(output)
