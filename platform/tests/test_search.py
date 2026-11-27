"""Testovi za pretragu grafa"""

from datetime import date

from sok.api import Edge, Graph, Node
from sok.core.search import search


def make_graph(directed: bool = True) -> Graph:
    """Graf sa tri osobe i jednim cvorom bez atributa, grane 1->2, 2->3, 1->3"""
    graph = Graph(directed=directed)
    alice = Node("1", {"name": "Alice", "age": 25})
    tom = Node("2", {"name": "Tom", "city": "Novi Sad"})
    ana = Node("3", {"name": "Ana", "age": 31, "birth_date": date(1995, 5, 17)})
    graph.add_node(alice)
    graph.add_node(tom)
    graph.add_node(ana)
    graph.add_node(Node("4"))
    graph.add_edge(Edge("12", alice, tom))
    graph.add_edge(Edge("23", tom, ana))
    graph.add_edge(Edge("13", alice, ana))
    return graph


def node_ids(graph: Graph) -> set:
    return {node.id for node in graph.nodes}


def edge_ids(graph: Graph) -> set:
    return {edge.id for edge in graph.edges}


def test_search_by_attribute_value():
    assert node_ids(search(make_graph(), "Alice")) == {"1"}


def test_search_by_part_of_value():
    assert node_ids(search(make_graph(), "Sad")) == {"2"}


def test_search_by_attribute_name():
    assert node_ids(search(make_graph(), "age")) == {"1", "3"}


def test_search_ignores_case():
    assert node_ids(search(make_graph(), "aLiCe")) == {"1"}


def test_search_number_as_text():
    assert node_ids(search(make_graph(), "31")) == {"3"}


def test_search_date_as_text():
    assert node_ids(search(make_graph(), "1995-05")) == {"3"}


def test_search_without_match_returns_empty_graph():
    result = search(make_graph(), "xyz")

    assert result.nodes == []
    assert result.edges == []


def test_result_keeps_only_edges_between_found_nodes():
    result = search(make_graph(), "age")

    assert edge_ids(result) == {"13"}


def test_result_keeps_directed():
    assert search(make_graph(directed=False), "age").directed is False


def test_search_does_not_change_original_graph():
    graph = make_graph()

    search(graph, "Alice")

    assert node_ids(graph) == {"1", "2", "3", "4"}
    assert len(graph.edges) == 3


def test_search_on_search_result():
    first = search(make_graph(), "a")

    assert node_ids(search(first, "age")) == {"1", "3"}


def test_empty_query_returns_whole_graph():
    result = search(make_graph(), "")

    assert node_ids(result) == {"1", "2", "3", "4"}
    assert edge_ids(result) == {"12", "23", "13"}


def test_query_with_only_spaces_returns_whole_graph():
    assert node_ids(search(make_graph(), "   ")) == {"1", "2", "3", "4"}
