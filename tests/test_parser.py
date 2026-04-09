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

def test_2():
    print(toTurtle("Alice homepage <https://example.org/~alice>"))

def test31():
    print(toTurtle("<x:a> <x:b> <x:c>"))

def test_noderefs():
    print(toTurtle("(1) implies -> (2)"))

def test_model():
    print(toTurtle("""
        @prefix https://example.org/model#
        
        TeamMember a Class
        
        TeamLead a Class
            subClassOf -> TeamMember
    """))



def toTurtle(src):
    g = graffl.parser.parse(src)
    ttl = g.serialize(format="turtle")
    return ttl
