"""Graf: skup cvorova i grana"""

from typing import Iterable, List

from .edge import Edge
from .node import Node


class Graph:
    """
    Genericki graf koji podrzava sve tipove grafova: usmerene i neusmerene,
    ciklicne i aciklicne, povezane i nepovezane

    Graf je vlasnik cvorova i grana i cuva pravila: id-jevi su jedinstveni,
    grana moze povezati samo cvorove koji su u grafu, a cvor se moze obrisati
    tek kad nema nijednu granu

    Primer::
        graph = Graph(directed=True)
        graph.add_node(Node("1", {"name": "Alice"}))
        graph.add_node(Node("2", {"name": "Tom"}))
        graph.add_edge(Edge("1", graph.get_node("1"), graph.get_node("2")))
    """

    def __init__(self, directed: bool = True):
        """
        :param directed: True za usmeren graf, False za neusmeren
        :type directed: bool
        """
        raise NotImplementedError

    @property
    def directed(self) -> bool:
        """
        :return: True ako je graf usmeren
        :rtype: bool
        """
        raise NotImplementedError

    @property
    def nodes(self) -> List[Node]:
        """
        :return: svi cvorovi grafa (nova lista, izmena liste ne menja graf)
        :rtype: List[Node]
        """
        raise NotImplementedError

    @property
    def edges(self) -> List[Edge]:
        """
        :return: sve grane grafa (nova lista, izmena liste ne menja graf)
        :rtype: List[Edge]
        """
        raise NotImplementedError

    # --- Cvorovi ---

    def add_node(self, node: Node) -> None:
        """
        :param node: cvor koji se dodaje
        :type node: Node
        :raises DuplicateNodeError: ako u grafu vec postoji cvor sa istim id-jem
        """
        raise NotImplementedError

    def has_node(self, node_id: str) -> bool:
        """
        :param node_id: id cvora
        :type node_id: str
        :return: True ako cvor postoji u grafu
        :rtype: bool
        """
        raise NotImplementedError

    def get_node(self, node_id: str) -> Node:
        """
        :param node_id: id cvora
        :type node_id: str
        :return: cvor sa tim id-jem
        :rtype: Node
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        raise NotImplementedError

    def remove_node(self, node_id: str) -> None:
        """
        Brise cvor iz grafa
        Cvor mora prethodno biti odvojen od svih grana

        :param node_id: id cvora koji se brise
        :type node_id: str
        :raises NodeNotFoundError: ako cvor ne postoji
        :raises NodeHasEdgesError: ako je cvor povezan bar jednom granom
        """
        raise NotImplementedError

    # --- Grane ---

    def add_edge(self, edge: Edge) -> None:
        """
        :param edge: Grana koja se dodaje. Oba njena čvora moraju već biti u grafu
        :type edge: Edge
        :raises DuplicateEdgeError: Ako u grafu već postoji grana sa istim id-jem
        :raises NodeNotFoundError: Ako source ili target nije u grafu
        """
        raise NotImplementedError

    def has_edge(self, edge_id: str) -> bool:
        """
        :param edge_id: Id grane
        :type edge_id: str
        :return: True ako grana postoji u grafu
        :rtype: bool
        """
        raise NotImplementedError

    def get_edge(self, edge_id: str) -> Edge:
        """
        :param edge_id: Id grane
        :type edge_id: str
        :return: Grana sa tim id-jem
        :rtype: Edge
        :raises EdgeNotFoundError: Ako grana ne postoji
        """
        raise NotImplementedError

    def remove_edge(self, edge_id: str) -> None:
        """
        :param edge_id: Id grane koja se briše
        :type edge_id: str
        :raises EdgeNotFoundError: Ako grana ne postoji
        """
        raise NotImplementedError

    # --- Susedstvo ---

    def edges_of(self, node_id: str) -> List[Edge]:
        """
        Vraca sve grane povezane sa cvorom, bez obzira na smer

        :param node_id: id cvora
        :type node_id: str
        :return: ulazne i izlazne grane cvora (petlja se pojavljuje jednom)
        :rtype: List[Edge]
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        raise NotImplementedError

    def outgoing_edges(self, node_id: str) -> List[Edge]:
        """
        U usmerenom grafu vraca grane kojima je cvor source
        U neusmerenom grafu vraca isto što i edges_of

        :param node_id: id cvora
        :type node_id: str
        :rtype: List[Edge]
        :raises NodeNotFoundError: Ako cvor ne postoji
        """
        raise NotImplementedError

    def incoming_edges(self, node_id: str) -> List[Edge]:
        """
        U usmerenom grafu vraca grane kojima je cvor target
        U neusmerenom grafu vraca isto sto i edges_of

        :param node_id: id cvora
        :type node_id: str
        :rtype: List[Edge]
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        raise NotImplementedError

    def neighbors(self, node_id: str) -> List[Node]:
        """
        Vraca cvorove do kojih se iz datog cvora stize jednom granom
        U usmerenom grafu to su target cvorovi izlaznih grana, a u neusmerenom
        cvorovi sa druge strane svake grane, svaki sused se pojavljuje jednom

        :param node_id: id cvora
        :type node_id: str
        :rtype: List[Node]
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        raise NotImplementedError

    # --- Ceo graf metode ---

    def subgraph(self, node_ids: Iterable[str]) -> "Graph":
        """
        Pravi novi graf od datih cvorova i svih grana cija su oba kraja medju njima

        Koristi se za rezultat pretrage i filtriranja
        Novi graf ima isti directed i deli iste objekte cvorova i grana sa originalnim grafom
        Id-jevi koji ne postoje u grafu se zanemaruju

        :param node_ids: id-jevi cvorova koji ulaze u podgraf
        :type node_ids: Iterable[str]
        :return: novi graf
        :rtype: Graph
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Brise sve cvorove i grane iz grafa"""
        raise NotImplementedError

    def is_connected(self) -> bool:
        """
        Proverava da li se od svakog cvora moze stici do svakog drugog,
        pri cemu se smer grana zanemaruje
        Prazan graf se smatra povezanim

        :rtype: bool
        """
        raise NotImplementedError

    def has_cycle(self) -> bool:
        """
        Proverava da li graf sadrzi ciklus

        U usmerenom grafu ciklus prati smer grana (npr. A->B->A)
        U neusmerenom jedna grana A-B nije ciklus,
        ali petlja ili dve grane izmedju istih cvorova jesu

        :rtype: bool
        """
        raise NotImplementedError