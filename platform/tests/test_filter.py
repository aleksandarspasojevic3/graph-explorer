"""Testovi za filtriranje grafa"""

from datetime import date, datetime

import pytest

from sok.api import Edge, Graph, Node
from sok.core.exceptions import InvalidQueryError
from sok.core.filter import filter_graph


def make_graph(directed: bool = True) -> Graph:
    """Graf sa tri osobe i jednim cvorom bez atributa, grane 1->2, 2->3, 1->3"""
    graph = Graph(directed=directed)
    alice = Node("1", {"name": "Alice", "age": 25, "height": 1.70, "birth_date": date(1999, 1, 10)})
    tom = Node("2", {"name": "Tom", "age": 30, "height": 1.85, "birth_date": date(1994, 3, 3)})
    ana = Node("3", {"name": "Ana", "age": 31, "height": 1.62, "birth_date": date(1995, 5, 17)})
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


@pytest.mark.parametrize("query, expected", [
    ("age == 30", {"2"}),
    ("age != 30", {"1", "3"}),
    ("age > 30", {"3"}),
    ("age >= 30", {"2", "3"}),
    ("age < 30", {"1"}),
    ("age <= 30", {"1", "2"}),
])
def test_every_comparator_on_int(query, expected):
    assert node_ids(filter_graph(make_graph(), query)) == expected


def test_int_is_compared_as_number_not_text():
    # kao tekst bi "100" bio manji od "25", kao broj nije
    assert node_ids(filter_graph(make_graph(), "age < 100")) == {"1", "2", "3"}


def test_float():
    assert node_ids(filter_graph(make_graph(), "height > 1.7")) == {"2"}


def test_float_with_whole_number_in_query():
    assert node_ids(filter_graph(make_graph(), "height < 2")) == {"1", "2", "3"}


def test_date():
    assert node_ids(filter_graph(make_graph(), "birth_date < 1995-01-01")) == {"2"}


def test_datetime():
    graph = Graph()
    graph.add_node(Node("1", {"created": datetime(2020, 5, 1, 10, 30)}))
    graph.add_node(Node("2", {"created": datetime(2019, 1, 1)}))

    assert node_ids(filter_graph(graph, "created >= 2020-01-01")) == {"1"}


@pytest.mark.parametrize("query", ["name == alice", "name == ALICE", "name == Alice"])
def test_text_ignores_case(query):
    assert node_ids(filter_graph(make_graph(), query)) == {"1"}


def test_text_not_equal_ignores_case():
    assert node_ids(filter_graph(make_graph(), "name != alice")) == {"2", "3"}


def test_text_less_than_ignores_case():
    assert node_ids(filter_graph(make_graph(), "name < bob")) == {"1", "3"}


def test_node_without_attribute_is_not_in_result():
    assert node_ids(filter_graph(make_graph(), "age >= 0")) == {"1", "2", "3"}


def test_missing_attribute_in_all_nodes_returns_empty_graph():
    result = filter_graph(make_graph(), "city == Novi Sad")

    assert result.nodes == []
    assert result.edges == []


def test_result_keeps_only_edges_between_found_nodes():
    result = filter_graph(make_graph(), "age >= 30")

    assert {edge.id for edge in result.edges} == {"23"}


def test_result_keeps_directed():
    assert filter_graph(make_graph(directed=False), "age > 0").directed is False


def test_filter_does_not_change_original_graph():
    graph = make_graph()

    filter_graph(graph, "age > 30")

    assert node_ids(graph) == {"1", "2", "3", "4"}
    assert len(graph.edges) == 3


@pytest.mark.parametrize("query", [
    "age > abc",
    "age > 25.5",
    "height > abc",
    "birth_date < 17.05.1995",
])
def test_value_of_wrong_type_raises_error(query):
    with pytest.raises(InvalidQueryError):
        filter_graph(make_graph(), query)


def test_error_message_contains_value_attribute_and_type():
    with pytest.raises(InvalidQueryError, match="'abc'.*'age'.*int"):
        filter_graph(make_graph(), "age > abc")


def test_mixed_types_raise_error_if_any_node_fails():
    graph = Graph()
    graph.add_node(Node("1", {"age": 25}))
    graph.add_node(Node("2", {"age": "nepoznato"}))

    with pytest.raises(InvalidQueryError):
        filter_graph(graph, "age > abc")


def test_invalid_query_raises_error():
    with pytest.raises(InvalidQueryError):
        filter_graph(make_graph(), "age = 25")
