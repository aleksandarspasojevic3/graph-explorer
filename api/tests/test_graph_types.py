"""Testovi da model podrzava sve tipove grafova - usmerene i neusmerene,
ciklicne i aciklicne, povezane i nepovezane"""

import pytest

from sok.api import Edge, Graph, Node


@pytest.mark.parametrize("fixture_name, directed, cyclic, connected", [
    ("people_graph", True, True, True),
    ("directed_acyclic_graph", True, False, True),
    ("undirected_tree", False, False, True),
    ("undirected_cyclic_graph", False, True, True),
    ("disconnected_graph", True, False, False),
    ("empty_graph", True, False, True),
])
def test_graph_types(request, fixture_name, directed, cyclic, connected):
    graph = request.getfixturevalue(fixture_name)

    assert graph.directed is directed
    assert graph.has_cycle() is cyclic
    assert graph.is_connected() is connected


def make_graph(directed, edges):
    """Pomocna funkcija - graf od liste grana zadatih kao (id source cvora, id target cvora)"""
    graph = Graph(directed=directed)
    for source_id, target_id in edges:
        for node_id in (source_id, target_id):
            if not graph.has_node(node_id):
                graph.add_node(Node(node_id))
    for index, (source_id, target_id) in enumerate(edges):
        graph.add_edge(Edge(str(index), graph.get_node(source_id), graph.get_node(target_id)))
    return graph


@pytest.mark.parametrize("directed, edges, cyclic", [
    (True, [("A", "A")], True),                   # petlja je ciklus
    (True, [("A", "B"), ("B", "A")], True),       # A -> B -> A
    (True, [("A", "B"), ("A", "B")], False),      # dve grane u istom smeru nisu ciklus
    (False, [("A", "A")], True),                  # petlja je ciklus i u neusmerenom
    (False, [("A", "B")], False),                 # jedna grana nije ciklus
    (False, [("A", "B"), ("B", "A")], True),      # dve grane izmedju istih cvorova jesu
])
def test_has_cycle_special_cases(directed, edges, cyclic):
    assert make_graph(directed, edges).has_cycle() is cyclic


def test_connectivity_ignores_direction():
    graph = make_graph(True, [("A", "B"), ("C", "B")])

    assert graph.is_connected()


def test_removing_edge_breaks_cycle(people_graph):
    people_graph.remove_edge("12")

    assert not people_graph.has_cycle()


def test_removing_edge_disconnects_graph(undirected_tree):
    undirected_tree.remove_edge("3")

    assert not undirected_tree.is_connected()