import graffl.parser
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def test_empty():
    print(toTurtle(""))


def test_simple():
    print(toTurtle("A"))


def test_simple_noderef_1():
    print(toTurtle("(A)"))


def test_simple_noderef_2():
    print(toTurtle("""
        (person001)
            label "Alice"
        
        (person002)
            label "Alice"
        
        (person001) knows -> (person002)
  
        """))


def test_simple_string():
    print(toTurtle("\"A\""))


def test_simple_mls_string():
    print(toTurtle("\"\"\"A\"\"\""))


def test_hello_world():
    print(toTurtle("World says Hello!"))


def test_1():
    print(toTurtle("Alice likes -> Bob"))


def test_uri_value():
    print(toTurtle("Alice homepage <https://example.org/~alice>"))


def test_number_value():
    print(toTurtle("x  y -3e+10"))


def test_only_uris():
    print(toTurtle("<http://example.org/subject> <http://example.org/predicate> <http://example.org/object>"))


def test_noderefs():
    print(toTurtle("(1) implies -> (2)"))


def test_noderef_as_value():
    print(toTurtle("(1) implies (2)"))


def test_prefix():
    print(toTurtle("""
    @prefix <http://example.org/ns#>
        "Mr. Bean"
    """))


def test_model():
    print(toTurtle("""
@prefix <http://example.org/pizza#>
@use RDFSchema
@use OWL

SalamiPizza : Class
    subClassOf [ : Class
        label "Pizza with Salami + Mozzarella"
        intersectionOf *(
            Pizza
            [ : Restriction
                onProperty hasTopping
                someValuesFrom Salami
            ]
            [ : Restriction
                onProperty hasTopping
                someValuesFrom Mozzarella
            ]
        )
    ]    """))


def test_model_2():
    print(toTurtle("""
@ prefix <http://example.org/ns#>
@ my = <http://example.org/ns#>
@ use RDFSchema
@ use OWL
@ use SHACL

MyClass : Class
    subClassOf [
        label "status ACTIVE"
         : Restriction
        onProperty status
        owl:hasValue "ACTIVE"
        ]

"status ACTIVE" : NodeShape
    targetClass MyClass
    property [ : PropertyShape
        path status
        sh:hasValue "ACTIVE"
    ]
     """))



def test_group_graph():
    print(toTurtle("""
        
    ---- Team-1 ----
        Alice

        Bob
    ----------------

    Team-1 worksWith -> Team-2

    ---- Team-2 ----
        Chris

        David
    ----------------

    ---- "The Agile Release Train" ----

        Team-1

        Team-2

    ----------------------------------
    """))


def test_blank_nodes():
    print(toTurtle("""
        Alice fullName [ firstName "Alice"
                         secondName "Jane" ]
    """))


def test_container():
    print(toTurtle("""
        "action items"
            * §1.1
            * §2.7
            * §3.21
    
        list1 has [
            * item1
            * item2
            * item3
            ]
    """))


def test_list_1():
    print(toTurtle("""
      Rainbow colors -> *( Red Green Blue )
    """))


def test_list_2():
    print(toTurtle("""
      Rainbow colors *( Red Green Blue )
    """))


def test_value():
    print(toTurtle("""
        §1 = " bla bla bla "
    """))


def test_seq():
    print(toTurtle("""
        (Tasks)
          1. Beginn
          2. "do something"
          * Break
          99. Done
    """))


def test_define_dict():
    print(toTurtle("""
        @ Alice = urn:example.org:persons:12345
        @ Bob   = urn:example.org:persons:67890
        @ likes = http://purl.org/spar/cito/likes
        
        Alice likes -> Bob
    """))


def test_languages():
    print(toTurtle("""
        (a)     label @de Adelheid
                label Alice
                label @es Alicia
                label @tlh QelIS
    """))


def test_datatypes():
    print(toTurtle(""" 
    Event
      name @en "Launch Party"
      startDate @dateTime "2023-11-01T12:00:00"
      participantCount @integer 42
      isPublic @boolean true      
    """))


def test_uri_predicate():
    print(toTurtle("""
        @ state : URI
        
        Alice state ACTIVE
        """))


def test_namespaces():
    print(toTurtle("""
@ ex = <http://example.org/persons#>

Alice : foaf:Person
    schema:name "Alice Müller"
    foaf:knows -> ex:Bob
        """))


def toTurtle(src):
    g = graffl.parser.parse(src)
    ttl = g.serialize(format="turtle")
    return ttl
