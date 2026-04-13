import graffl.parser


def test_empty():
    print(toTurtle(""))


def test_simple():
    print(toTurtle("A"))


def test_simple_noderef():
    print(toTurtle("(A)"))


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

<http://example.org/pizza#>
    : Ontology
    label "Die Erweiterte Pizza-Ontologie"
    comment "Ein komplexer Härtetest für den Graffl-Parser mit OWL DL."

---- "Eigenschaften" ----

hasTopping
    : ObjectProperty
    label "hat Belag"

hasBase
    : ObjectProperty
    label "hat Boden"

-------------------------

---- "Grundzutaten" ----

PizzaBase : Class

PizzaTopping : Class

CheeseTopping 
    : Class
    subClassOf PizzaTopping
    
MeatTopping 
    : Class
    subClassOf PizzaTopping
    disjointWith CheeseTopping
    
Mozzarella
    : Class
    subClassOf CheeseTopping
    
Salami
    : Class
    subClassOf MeatTopping
    
Ham
    : Class
    subClassOf MeatTopping
    
Jalapeno
    : Class
    subClassOf PizzaTopping

------------------------

---- "Komplexe Pizzen" ----

Pizza : Class

SalamiPizza
    : Class
    subClassOf [
        : Class
        intersectionOf *(
            Pizza
            [
                : Restriction
                onProperty hasTopping
                someValuesFrom Salami
            ]
            [
                : Restriction
                onProperty hasTopping
                someValuesFrom Mozzarella
            ]
        )
    ]

SpicyPizza
    : Class
    equivalentClass [
        : Class
        intersectionOf *(
            Pizza
            [
                : Restriction
                onProperty hasTopping
                someValuesFrom Jalapeno
            ]
        )
    ]

MeatLoversPizza
    : Class
    subClassOf [
        : Class
        intersectionOf *(
            Pizza
            [
                : Restriction
                onProperty hasTopping
                someValuesFrom [
                    : Class
                    unionOf *( Salami Ham )
                ]
            ]
        )
    ]

---------------------------
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
        Alice fullName [
            firstName "Alice"
            secondName "Jane"
            lastName "Van Houten"
        ]
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
          99. Done
    """))


def test_define_dict():
    print(toTurtle("""
        @x = <http://www.example.org/x>
        @y = <http://fowf#y>
        @z = <urn:z>
        
        x y -> z
        
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
          participantCount @integer "42"
          isPublic @boolean "true"          
    """))


def test_uri_predicate():
    print(toTurtle("""
        @ state : URI
        
        Alice state ACTIVE
        """))

def toTurtle(src):
    g = graffl.parser.parse(src)
    ttl = g.serialize(format="turtle")
    return ttl

