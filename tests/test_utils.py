import pytest
from rdflib import Dataset
from rdflib.compare import isomorphic, graph_diff
import graffl.parser


def assert_graffl_matches(graffl_src: str, expected_rdf: str, rdf_format: str = "trig"):
    actual_dataset = graffl.parser.parse(graffl_src)

    ttl = actual_dataset.serialize(format="trig")
    print(ttl)

    expected_dataset = Dataset()
    expected_dataset.parse(data=expected_rdf, format=rdf_format)

    # 1. Ensure both datasets have the same named graphs (contexts)
    actual_contexts = set(g.identifier for g in actual_dataset.contexts())
    expected_contexts = set(g.identifier for g in expected_dataset.graphs())

    if actual_contexts != expected_contexts:
        pytest.fail(
            f"Different Named Graphs (Contexts) found!\n"
            f"Expected: {expected_contexts}\n"
            f"Actual: {actual_contexts}"
        )

    # 2. Check graphs individually for isomorphism
    for ctx_id in expected_contexts:
        actual_g = actual_dataset.get_context(ctx_id)
        expected_g = expected_dataset.get_context(ctx_id)

        if not isomorphic(actual_g, expected_g):
            _, in_actual_only, in_expected_only = graph_diff(actual_g, expected_g)

            # Error handling: Precise diff for the failing graph
            graph_name = "Default Graph" if ctx_id == expected_dataset.default_graph.identifier else f"Named Graph <{ctx_id}>"

            error_msg = f"Asserted and expected graphs {graph_name} are not isomorphic!\n\n"
            pytest.fail(error_msg)