"""Testovi za grane cvora, susede i podgraf"""

import pytest

from sok.api import NodeNotFoundError


def ids(elements):
    """Pomocna funkcija - skup id-jeva cvorova ili grana"""
    return {element.id for element in elements}


def test_edges_of_ignores_direction(people_graph):
    assert ids(people_graph.edges_of("1")) == {"10", "12", "13"}


def test_outgoing_and_incoming_edges_in_directed_graph(people_graph):
    assert ids(people_graph.outgoing_edges("1")) == {"10", "13"}
    assert ids(people_graph.incoming_edges("1")) == {"12"}


def test_outgoing_and_incoming_edges_in_undirected_graph(undirected_tree):
    assert ids(undirected_tree.outgoing_edges("B")) == {"1", "2", "3"}
    assert ids(undirected_tree.incoming_edges("B")) == {"1", "2", "3"}


def test_neighbors_in_directed_graph_follow_direction(people_graph):
    assert ids(people_graph.neighbors("1")) == {"2", "4"}


def test_neighbors_in_undirected_graph(undirected_tree):
    assert ids(undirected_tree.neighbors("B")) == {"A", "C", "D"}
    assert ids(undirected_tree.neighbors("A")) == {"B"}


def test_isolated_node_has_no_neighbors(disconnected_graph):
    assert disconnected_graph.neighbors("E") == []


@pytest.mark.parametrize("method", ["edges_of", "outgoing_edges", "incoming_edges", "neighbors"])
def test_missing_node_raises(people_graph, method):
    with pytest.raises(NodeNotFoundError):
        getattr(people_graph, method)("99")


def test_subgraph_keeps_edges_between_selected_nodes(people_graph):
    subgraph = people_graph.subgraph(["1", "2", "3"])

    assert ids(subgraph.nodes) == {"1", "2", "3"}
    assert ids(subgraph.edges) == {"10", "11", "12"}
    assert subgraph.directed == people_graph.directed


def test_subgraph_ignores_missing_ids(people_graph):
    subgraph = people_graph.subgraph({"1", "99"})

    assert ids(subgraph.nodes) == {"1"}
    assert subgraph.edges == []


def test_subgraph_shares_objects_with_original(people_graph):
    subgraph = people_graph.subgraph(["1"])

    subgraph.get_node("1").set_attribute("age", 99)

    assert people_graph.get_node("1").get_attribute("age") == 99


def test_subgraph_does_not_change_original(people_graph):
    people_graph.subgraph(["1"]).clear()

    assert len(people_graph.nodes) == 4


def test_subgraph_of_subgraph(people_graph):
    result = people_graph.subgraph(["1", "2", "3"]).subgraph(["1", "2"])

    assert ids(result.nodes) == {"1", "2"}
    assert ids(result.edges) == {"10"}