import graffl.parser

def test_empty():
    print(toTurtle(""))

def test_simple():
    print(toTurtle("A"))

def test_simple_noderef():
    print(toTurtle("(A)"))

def test_hello_world():
    print(toTurtle("World says Hello!"))

def test_1():
    print(toTurtle("Alice likes -> Bob"))

def test_uri_value():
    print(toTurtle("Alice homepage <https://example.org/~alice>"))

def test_only_uris():
    print(toTurtle("<http://example.org/subject> <http://example.org/predicate> <http://example.org/object>"))

def test_noderefs():
    print(toTurtle("(1) implies -> (2)"))

def test_noderef_as_value():
    print(toTurtle("(1) implies (2)"))

def test_model():
    print(toTurtle("""
        @prefix https://example.org/model#
        
        TeamMember a Class
        
        TeamLead a Class
            subClassOf -> TeamMember
    """))


def test_group_graph():
    print(toTurtle("""
        
    ----"Group 1"-----
    
    A
    
    B
    
    ------------------
    
    
    ----<urn:group-2>-----
    
    ----------------------
    
    
    ---- Group-3 ---------
    
    ----------------------
    
    
    
    ---- (Group 4) ---------
    
    A
    
    B
    
    ------------------------
    """))


def test_blank_nodes    ():
    print(toTurtle("""
        (A) hasSomething [
                with1 "X"
                with2 [
                    with3 <urn:Z>
                ]
            ]
    """))



def test_list():
    print(toTurtle("""
        "action items"
            - "do 1"
            - "do 2"
            - "do 3"
    
        list1 has [
            - item1
            sublist [ - item3 - item4 ]
            - item2
            ]
    """))


def toTurtle(src):
    g = graffl.parser.parse(src)
    ttl = g.serialize(format="turtle")
    return ttl
