import pytest

import graffl.cli
import graffl.parser
from test_utils import assert_graffl_matches


def test_empty():
    assert_graffl_matches("", "")


def test_node_types_and_labels():
    # Tests different node declarations and automatic rdfs:label generation
    graffl_src = """
        @prefix <http://example.org/ns#>

        Alice
        
        "Mr. Bean"
        
        (nodeRef)
        
        <http://example.org/uri>
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Alice rdfs:label "Alice" .
        ns:Mr.%20Bean rdfs:label "Mr. Bean" .

        # Note: (nodeRef) and <http://example.org/uri> do not generate labels
        # unless they have explicit properties, so they remain empty nodes 
        # in this minimal snippet.
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_ml_string():
    graffl_src = """
           @prefix <http://example.org/ns#>

           (Alice) ; \"\"\"There are
many things to know
about
Alice...\"\"\"
       """

    expected_rdf = """
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

             <http://example.org/ns#Alice> rdfs:comment "\"\"There are
many things to know
about
Alice...\"\"\" .
        """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_basic_relations_and_properties():
    # Tests literal properties vs relations (->)
    graffl_src = """
        @prefix <http://example.org/ns#>

        Alice likes -> Bob
            email "alice@example.org"
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Alice rdfs:label "Alice" ;
                 ns:likes ns:Bob ;
                 ns:email "alice@example.org" .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_namespaces_and_qnames():
    # Tests predefined namespaces and dynamic QName resolution
    graffl_src = """
        @ ex = <http://example.org/persons#>
        @prefix <http://example.org/ns#>

        Alice type foaf:Person
            foaf:knows -> ex:Bob
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix ex: <http://example.org/persons#> .
        @prefix foaf: <http://xmlns.com/foaf/0.1/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        ns:Alice rdfs:label "Alice" ;
                 rdf:type foaf:Person ;
                 foaf:knows ex:Bob .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_datatypes():
    # Tests XSD datatype tagging (@dateTime, @integer, etc.)
    graffl_src = """
        @prefix <http://example.org/ns#>

        Event
            startDate @dateTime "2023-11-01T12:00:00"
            participantCount @integer 42
            isPublic @boolean true
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Event rdfs:label "Event" ;
                 ns:startDate "2023-11-01T12:00:00"^^xsd:dateTime ;
                 ns:participantCount "42"^^xsd:integer ;
                 ns:isPublic "true"^^xsd:boolean .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_languages():
    # Tests ISO language tagging (@en, @de, etc.)
    graffl_src = """
        @prefix <http://example.org/ns#>

        (a) label @en Alice
            label @tlh QelIS
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:a rdfs:label "Alice"@en, "QelIS"@tlh .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_uri_properties_and_aliases():
    # Tests the declaration of a predicate as a URI property and custom aliases
    graffl_src = """
        @prefix <http://example.org/ns#>
        @ state : URI
        @ ACTIVE = <urn:state:active>

        Alice state ACTIVE
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Alice rdfs:label "Alice" ;
                 ns:state <urn:state:active> .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_blank_nodes():
    # Tests nested anonymous nodes
    graffl_src = """
        @prefix <http://example.org/ns#>

        Alice fullName [ firstName "Alice"
                         secondName "Jane" ]
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Alice rdfs:label "Alice" ;
                 ns:fullName [ 
                     ns:firstName "Alice" ;
                     ns:secondName "Jane" 
                 ] .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_containers():
    # Tests rdf:li (*) and rdf:_N (1., 2.) enumerations
    graffl_src = """
        @prefix <http://example.org/ns#>

        (Tasks)
            1. Beginn
            2. "do something"
            * Break
            99. Done
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        ns:Tasks rdf:_1 "Beginn" ;
                 rdf:_2 "do something" ;
                 rdf:_99 "Done" ;
                 rdf:li "Break" .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_lists():
    # Tests proper RDF Collections (Linked Lists)
    # rdflib natively understands the ( ... ) syntax in Turtle for lists
    graffl_src = """
        @prefix <http://example.org/ns#>

        Rainbow colors -> *( Red Green Blue )
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Rainbow rdfs:label "Rainbow" ;
                   ns:colors ( ns:Red ns:Green ns:Blue ) .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_named_graphs():
    # Tests context mapping to named graphs in the Dataset
    graffl_src = """
        @context <http://example.org/mygraph>
        @prefix <http://example.org/ns#>

        Alice likes -> Bob
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        <http://example.org/mygraph> {
            ns:Alice rdfs:label "Alice" ;
                     ns:likes ns:Bob .
        }
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_group_graphs():
    # Tests logical grouping and the automatic "contains" relationship
    graffl_src = """
        @prefix <http://example.org/ns#>

        ---- Team-1 ----
            Alice

            Bob
        ----------------
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix graffl: <https://www.hedenus.de/graffl/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Team-1 a graffl:Group ;
                  rdfs:label "Team-1" ;
                  graffl:contains ns:Alice, ns:Bob .

        ns:Alice rdfs:label "Alice" .
        ns:Bob rdfs:label "Bob" .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_list_in_group_graphs():
    graffl_src = """
        @prefix <http://example.org/ns#>

        ---- Team-1 ----
            (Alice) likes *( Pizza Coke )
        ----------------
    """

    expected_rdf = """
        @prefix ns1: <http://example.org/ns#> .
        @prefix graffl: <https://www.hedenus.de/graffl/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    ns1:Team-1 a graffl:Group ;
        rdfs:label "Team-1" ;
        graffl:contains
            ns1:Alice,
            _:BN1,
            _:BN2 .

    ns1:Alice ns1:likes _:BN1 .

    _:BN1 rdf:first "Pizza" ;
        rdf:rest _:BN2 .

    _:BN2 rdf:first "Coke" ;
        rdf:rest () .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_profile_loader_with_yaml(tmp_path):
    # 1. Create a temporary YAML profile
    profile_content = """
    dictionary:
      customRel: "http://example.org/custom/relation"
    vocabularies:
      "http://example.org/vocab#":
        - MyCustomClass
    uri_properties:
      - "http://example.org/custom/relation"
    """
    # Write it to the temporary test directory
    profile_path = tmp_path / "test_profile.yaml"
    profile_path.write_text(profile_content, encoding="utf-8")

    # 2. Graffl source using the absolute path to the temp profile
    # Use explicit prefix to avoid UUIDs
    graffl_src = f"""
        @ prefix <http://example.org/ns#>
        @ use {profile_path.as_posix()}

        Alice type MyCustomClass
            customRel -> Bob
    """

    # 3. Expected RDF
    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        ns:Alice rdfs:label "Alice" ;
                 rdf:type <http://example.org/vocab#MyCustomClass> ;
                 <http://example.org/custom/relation> ns:Bob .
    """

    assert_graffl_matches(graffl_src, expected_rdf)


def test_parser_syntax_error():
    # Expect a ValueError containing "Syntax error"
    with pytest.raises(ValueError, match="Syntax error"):
        # Invalid syntax: consecutive arrows
        graffl.parser.parse("Alice -> -> Bob")


def test_parser_empty_or_none():
    # Parsing None or an empty file should return an empty graph, not crash
    from rdflib import Dataset
    g = graffl.parser.parse("")
    assert isinstance(g, Dataset)
    assert len(g) == 0


def test_bnode_in_group_graphs():
    graffl_src = """
        @prefix <http://example.org/ns#>

        ---- "Example 1" ----
            
            (Alice) hasRole [ : Role = "Lead" ]
            
        ----------------
    """

    expected_rdf = """
            @prefix ns1: <https://www.hedenus.de/graffl/> .
            @prefix ns2: <http://example.org/ns#> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        
            ns2:Example%201 a ns1:Group ;
                rdfs:label "Example 1" ;
                ns1:contains  ns2:Alice, _:BN1 .
        
            ns2:Alice ns2:hasRole _:BN1 .
        
            _:BN1 a ns2:Role ; rdf:value "Lead" .
    """
    assert_graffl_matches(graffl_src, expected_rdf)


def test_comments():
    graffl_src = """
        @prefix <http://example.org/ns#>

        // This is a global comment at the top of the file
        Alice likes -> Bob

            // This is an indented comment inside a block
            Bob status "active"
    """

    expected_rdf = """
        @prefix ns: <http://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

        ns:Alice rdfs:label "Alice" ;
                 ns:likes ns:Bob .

        ns:Bob rdfs:label "Bob" ;
               ns:status "active" .
    """

    assert_graffl_matches(graffl_src, expected_rdf)