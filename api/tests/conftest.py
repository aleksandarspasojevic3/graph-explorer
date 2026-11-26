"""Testni grafovi za testove modela grafa

pytest sam ucitava ovaj fajl, svaka funkcija oznacena sa @pytest.fixture postaje
dostupna svim testovima u ovom folderu - test samo navede ime fixture-a kao parametar,
a pytest pozove funkciju i prosledi graf
Svaki test dobija nov, svez graf

Pregled grafova:

    graf                      usmeren  ciklican  povezan
    people_graph              da       da        da
    directed_acyclic_graph    da       ne        da
    undirected_tree           ne       ne        da
    undirected_cyclic_graph   ne       da        da
    disconnected_graph        da       ne        ne
    empty_graph               da       ne        da
"""

from datetime import date
from typing import Dict, List, Mapping, Optional, Tuple

import pytest

from sok.api import AttributeValue, Edge, Graph, Node

NodeSpec = Dict[str, Optional[Mapping[str, AttributeValue]]]
EdgeSpec = List[Tuple[str, str, str]]


def build_graph(directed: bool, nodes: NodeSpec, edges: EdgeSpec) -> Graph:
    """
    Pravi graf od opisa cvorova i grana

    :param directed: da li je graf usmeren
    :type directed: bool
    :param nodes: id cvora -> atributi cvora (ili None)
    :type nodes: Dict[str, Mapping[str, AttributeValue] | None]
    :param edges: lista grana kao (id grane, id source cvora, id target cvora)
    :type edges: List[Tuple[str, str, str]]
    :return: napravljen graf
    :rtype: Graph
    """
    graph = Graph(directed=directed)
    for node_id, attributes in nodes.items():
        graph.add_node(Node(node_id, attributes))
    for edge_id, source_id, target_id in edges:
        graph.add_edge(Edge(edge_id, graph.get_node(source_id), graph.get_node(target_id)))
    return graph


@pytest.fixture
def people_graph() -> Graph:
    """
    Usmeren, ciklican, povezan graf osoba sa atributima svih dozvoljenih tipova

        1 (Alice) -> 2 (Tom) -> 3 (Bob) -> 1 (Alice)     ciklus 1 -> 2 -> 3 -> 1
        1 (Alice) -> 4 (Ana)
    """
    graph = build_graph(
        directed=True,
        nodes={
            "1": {"name": "Alice", "age": 25, "height": 1.65, "born": date(2000, 5, 17)},
            "2": {"name": "Tom", "age": 30, "height": 1.82, "born": date(1995, 1, 3)},
            "3": {"name": "Bob", "age": 19, "height": 1.75, "born": date(2006, 11, 30)},
            "4": {"name": "Ana", "age": 42, "height": 1.70, "born": date(1983, 7, 9)},
        },
        edges=[("10", "1", "2"), ("11", "2", "3"), ("12", "3", "1"), ("13", "1", "4")],
    )
    graph.get_edge("10").set_attribute("relation", "friends")
    return graph


@pytest.fixture
def directed_acyclic_graph() -> Graph:
    """
    Usmeren, aciklican, povezan graf u obliku dijamanta

        A -> B -> D
        A -> C -> D
    """
    return build_graph(
        directed=True,
        nodes={"A": None, "B": None, "C": None, "D": None},
        edges=[("1", "A", "B"), ("2", "A", "C"), ("3", "B", "D"), ("4", "C", "D")],
    )


@pytest.fixture
def undirected_tree() -> Graph:
    """
    Neusmeren, aciklican, povezan graf (stablo)

        A - B - C
            |
            D
    """
    return build_graph(
        directed=False,
        nodes={"A": None, "B": None, "C": None, "D": None},
        edges=[("1", "A", "B"), ("2", "B", "C"), ("3", "B", "D")],
    )


@pytest.fixture
def undirected_cyclic_graph() -> Graph:
    """
    Neusmeren, ciklican, povezan graf: trougao A - B - C - A i cvor D zakacen na C
    """
    return build_graph(
        directed=False,
        nodes={"A": None, "B": None, "C": None, "D": None},
        edges=[("1", "A", "B"), ("2", "B", "C"), ("3", "C", "A"), ("4", "C", "D")],
    )


@pytest.fixture
def disconnected_graph() -> Graph:
    """
    Usmeren, aciklican, nepovezan graf sa tri komponente

        A -> B      C -> D      E (izolovan cvor)
    """
    return build_graph(
        directed=True,
        nodes={"A": None, "B": None, "C": None, "D": None, "E": None},
        edges=[("1", "A", "B"), ("2", "C", "D")],
    )


@pytest.fixture
def empty_graph() -> Graph:
    """Prazan usmeren graf, bez cvorova i grana"""
    return Graph()