"""Testovi za dodavanje, pronalazenje i brisanje cvorova i grana"""

import pytest

from sok.api import (
    DuplicateEdgeError,
    DuplicateNodeError,
    Edge,
    EdgeNotFoundError,
    Graph,
    Node,
    NodeHasEdgesError,
    NodeNotFoundError,
)


def test_new_graph_is_directed_by_default():
    assert Graph().directed is True
    assert Graph(directed=False).directed is False


def test_add_and_get_node(empty_graph):
    node = Node("1")

    empty_graph.add_node(node)

    assert empty_graph.has_node("1")
    assert empty_graph.get_node("1") is node
    assert empty_graph.nodes == [node]


def test_add_duplicate_node_raises(empty_graph):
    empty_graph.add_node(Node("1"))

    with pytest.raises(DuplicateNodeError):
        empty_graph.add_node(Node("1"))


def test_get_missing_node_raises(empty_graph):
    assert not empty_graph.has_node("1")
    with pytest.raises(NodeNotFoundError):
        empty_graph.get_node("1")


def test_nodes_returns_copy(people_graph):
    people_graph.nodes.clear()

    assert len(people_graph.nodes) == 4


def test_add_and_get_edge(empty_graph):
    a, b = Node("A"), Node("B")
    empty_graph.add_node(a)
    empty_graph.add_node(b)
    edge = Edge("1", a, b)

    empty_graph.add_edge(edge)

    assert empty_graph.has_edge("1")
    assert empty_graph.get_edge("1") is edge
    assert empty_graph.edges == [edge]


def test_add_duplicate_edge_raises(directed_acyclic_graph):
    a = directed_acyclic_graph.get_node("A")
    d = directed_acyclic_graph.get_node("D")

    with pytest.raises(DuplicateEdgeError):
        directed_acyclic_graph.add_edge(Edge("1", a, d))


def test_add_edge_with_node_outside_graph_raises(directed_acyclic_graph):
    a = directed_acyclic_graph.get_node("A")

    with pytest.raises(NodeNotFoundError):
        directed_acyclic_graph.add_edge(Edge("99", a, Node("X")))
    assert not directed_acyclic_graph.has_edge("99")


def test_loop_and_parallel_edges_are_allowed(empty_graph):
    a, b = Node("A"), Node("B")
    empty_graph.add_node(a)
    empty_graph.add_node(b)

    empty_graph.add_edge(Edge("1", a, a))
    empty_graph.add_edge(Edge("2", a, b))
    empty_graph.add_edge(Edge("3", a, b))

    assert len(empty_graph.edges) == 3


def test_get_missing_edge_raises(empty_graph):
    with pytest.raises(EdgeNotFoundError):
        empty_graph.get_edge("1")


def test_remove_edge(directed_acyclic_graph):
    directed_acyclic_graph.remove_edge("1")

    assert not directed_acyclic_graph.has_edge("1")
    assert len(directed_acyclic_graph.edges) == 3


def test_remove_missing_edge_raises(empty_graph):
    with pytest.raises(EdgeNotFoundError):
        empty_graph.remove_edge("1")


def test_remove_node_without_edges(disconnected_graph):
    disconnected_graph.remove_node("E")

    assert not disconnected_graph.has_node("E")


def test_remove_node_with_edges_raises(disconnected_graph):
    with pytest.raises(NodeHasEdgesError):
        disconnected_graph.remove_node("A")
    assert disconnected_graph.has_node("A")


def test_remove_node_after_removing_its_edges(disconnected_graph):
    disconnected_graph.remove_edge("1")

    disconnected_graph.remove_node("A")

    assert not disconnected_graph.has_node("A")


def test_remove_missing_node_raises(empty_graph):
    with pytest.raises(NodeNotFoundError):
        empty_graph.remove_node("1")


def test_clear(people_graph):
    people_graph.clear()

    assert people_graph.nodes == []
    assert people_graph.edges == []