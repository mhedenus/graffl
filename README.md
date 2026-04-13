<div>
  <img src="docs/graffl.png" alt="graffl Logo" width="400" />
</div>

(pronounced g-raffl, but also derived from the Bavarian 
word for "Graffl" for "stuff" or "junk")

__graffl__ is a (still) experimental __RDF__ scratch pad file format.
Its purpose is to write something down that is immediately
understood as graph data. No annoying syntax like dots or commas is required.
Think of it as Markdown for RDF.

For example, the following __graffl__ graph:

    Alice likes -> Bob

written as Turtle:

    @prefix ns1: <https://www.hedenus.de/graffl/76a04f61-342e-11f1-a289-e08f4ccbe174/> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    
    ns1:Alice rdfs:label "Alice" ;
        ns1:likes ns1:Bob .


It also supports nesting graphs, which is very useful for layouting.
See the `src/graffl/graffl.lark` file for the EBNF grammar.

See the documentation `docs/graffl.adoc`!

The parser is implemented as extension for __rdflib__: https://github.com/rdflib/rdflib

The file format is used by __rdf2graphml__: https://github.com/mhedenus/rdf2graphml
