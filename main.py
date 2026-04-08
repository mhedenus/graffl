from rdflib import Graph

import graffl.parser

g = Graph()

test_graffl_data = """
@ p1 p2 p3

    Michael : x
        "hat Geburtstag" 08.02.1974
        email michael@hedenus.de
        homepage https://www.hedenus.de#/~mhedenus/?q1=x1&q2=x2()#1
        mag -> Doris
    
    Doris
    

    
---- I1 ----
X

Y
------------



"""


g.parse(data=test_graffl_data, format="graffl")

for subj, pred, obj in g:
    print(f"Subjekt: {subj}, Prädikat: {pred}, Objekt: {obj}")
