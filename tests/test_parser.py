import graffl.parser


def test_hello_word():
    print(toTurtle("Word says Hello!"))

def test_1():
    print(toTurtle("Alice likes -> Bob"))

def test_2():
    print(toTurtle("Alice homepage <https://example.org/~alice>"))

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
