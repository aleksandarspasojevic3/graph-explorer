"""Graf: skup cvorova i grana"""

from collections import deque
from typing import Dict, Iterable, List, Set

from .edge import Edge
from .exceptions import (
    DuplicateEdgeError,
    DuplicateNodeError,
    EdgeNotFoundError,
    NodeHasEdgesError,
    NodeNotFoundError,
)
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
        self._directed = directed
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[str, Edge] = {}

    @property
    def directed(self) -> bool:
        """
        :return: True ako je graf usmeren
        :rtype: bool
        """
        return self._directed

    @property
    def nodes(self) -> List[Node]:
        """
        :return: svi cvorovi grafa (nova lista, izmena liste ne menja graf)
        :rtype: List[Node]
        """
        return list(self._nodes.values())

    @property
    def edges(self) -> List[Edge]:
        """
        :return: sve grane grafa (nova lista, izmena liste ne menja graf)
        :rtype: List[Edge]
        """
        return list(self._edges.values())

    # --- Cvorovi ---

    def add_node(self, node: Node) -> None:
        """
        :param node: cvor koji se dodaje
        :type node: Node
        :raises DuplicateNodeError: ako u grafu vec postoji cvor sa istim id-jem
        """
        if node.id in self._nodes:
            raise DuplicateNodeError(f"Cvor sa id-jem '{node.id}' vec postoji u grafu.")
        self._nodes[node.id] = node

    def has_node(self, node_id: str) -> bool:
        """
        :param node_id: id cvora
        :type node_id: str
        :return: True ako cvor postoji u grafu
        :rtype: bool
        """
        return node_id in self._nodes

    def get_node(self, node_id: str) -> Node:
        """
        :param node_id: id cvora
        :type node_id: str
        :return: cvor sa tim id-jem
        :rtype: Node
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        if node_id not in self._nodes:
            raise NodeNotFoundError(f"Cvor sa id-jem '{node_id}' ne postoji u grafu.")
        return self._nodes[node_id]

    def remove_node(self, node_id: str) -> None:
        """
        Brise cvor iz grafa
        Cvor mora prethodno biti odvojen od svih grana

        :param node_id: id cvora koji se brise
        :type node_id: str
        :raises NodeNotFoundError: ako cvor ne postoji
        :raises NodeHasEdgesError: ako je cvor povezan bar jednom granom
        """
        self.get_node(node_id)
        edges = self.edges_of(node_id)
        if edges:
            raise NodeHasEdgesError(
                f"Cvor '{node_id}' ne moze da se obrise jer ima {len(edges)} grana. "
                f"Prvo obrisite grane: {', '.join(edge.id for edge in edges)}.")
        del self._nodes[node_id]

    # --- Grane ---

    def add_edge(self, edge: Edge) -> None:
        """
        :param edge: grana koja se dodaje, oba njena cvora moraju vec biti u grafu
        :type edge: Edge
        :raises DuplicateEdgeError: ako u grafu vec postoji grana sa istim id-jem
        :raises NodeNotFoundError: ako source ili target nije u grafu
        """
        if edge.id in self._edges:
            raise DuplicateEdgeError(f"Grana sa id-jem '{edge.id}' vec postoji u grafu.")
        for endpoint in (edge.source, edge.target):
            if not self.has_node(endpoint.id):
                raise NodeNotFoundError(
                    f"Grana '{edge.id}' povezuje cvor '{endpoint.id}' koji nije u grafu.")
        self._edges[edge.id] = edge

    def has_edge(self, edge_id: str) -> bool:
        """
        :param edge_id: id grane
        :type edge_id: str
        :return: True ako grana postoji u grafu
        :rtype: bool
        """
        return edge_id in self._edges

    def get_edge(self, edge_id: str) -> Edge:
        """
        :param edge_id: id grane
        :type edge_id: str
        :return: Grana sa tim id-jem
        :rtype: Edge
        :raises EdgeNotFoundError: ako grana ne postoji
        """
        if edge_id not in self._edges:
            raise EdgeNotFoundError(f"Grana sa id-jem '{edge_id}' ne postoji u grafu.")
        return self._edges[edge_id]

    def remove_edge(self, edge_id: str) -> None:
        """
        :param edge_id: id grane koja se brise
        :type edge_id: str
        :raises EdgeNotFoundError: ako grana ne postoji
        """
        self.get_edge(edge_id)
        del self._edges[edge_id]

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
        self.get_node(node_id)
        return [edge for edge in self._edges.values()
                if edge.source.id == node_id or edge.target.id == node_id]

    def outgoing_edges(self, node_id: str) -> List[Edge]:
        """
        U usmerenom grafu vraca grane kojima je cvor source
        U neusmerenom grafu vraca isto sto i edges_of

        :param node_id: id cvora
        :type node_id: str
        :rtype: List[Edge]
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        if not self._directed:
            return self.edges_of(node_id)
        self.get_node(node_id)
        return [edge for edge in self._edges.values() if edge.source.id == node_id]

    def incoming_edges(self, node_id: str) -> List[Edge]:
        """
        U usmerenom grafu vraca grane kojima je cvor target
        U neusmerenom grafu vraca isto sto i edges_of

        :param node_id: id cvora
        :type node_id: str
        :rtype: List[Edge]
        :raises NodeNotFoundError: ako cvor ne postoji
        """
        if not self._directed:
            return self.edges_of(node_id)
        self.get_node(node_id)
        return [edge for edge in self._edges.values() if edge.target.id == node_id]

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
        neighbors: List[Node] = []
        seen = set()
        for edge in self.outgoing_edges(node_id):
            other = edge.target if edge.source.id == node_id else edge.source
            if other.id not in seen:
                seen.add(other.id)
                neighbors.append(other)
        return neighbors

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
        ids = set(node_ids)
        result = Graph(directed=self._directed)
        for node in self._nodes.values():
            if node.id in ids:
                result.add_node(node)
        for edge in self._edges.values():
            if edge.source.id in ids and edge.target.id in ids:
                result.add_edge(edge)
        return result

    def clear(self) -> None:
        """Brise sve cvorove i grane iz grafa"""
        self._nodes.clear()
        self._edges.clear()

    def is_connected(self) -> bool:
        """
        Proverava da li se od svakog cvora moze stici do svakog drugog,
        pri cemu se smer grana zanemaruje
        Prazan graf se smatra povezanim

        :rtype: bool
        """
        return self._count_components() <= 1

    def has_cycle(self) -> bool:
        """
        Proverava da li graf sadrzi ciklus

        U usmerenom grafu ciklus prati smer grana (npr. A->B->A)
        U neusmerenom jedna grana A-B nije ciklus,
        ali petlja ili dve grane izmedju istih cvorova jesu

        :rtype: bool
        """
        if self._directed:
            return self._has_directed_cycle()
        return len(self._edges) > len(self._nodes) - self._count_components()

    def _undirected_adjacency(self) -> Dict[str, Set[str]]:
        """Pomocna metoda: za svaki cvor vraca skup id-jeva suseda, pri cemu se smer grana zanemaruje"""
        adjacency: Dict[str, Set[str]] = {node_id: set() for node_id in self._nodes}
        for edge in self._edges.values():
            adjacency[edge.source.id].add(edge.target.id)
            adjacency[edge.target.id].add(edge.source.id)
        return adjacency

    def _count_components(self) -> int:
        """Pomocna metoda: broj komponenti povezanosti grafa, pri cemu se smer grana zanemaruje"""
        adjacency = self._undirected_adjacency()
        visited: Set[str] = set()
        components = 0
        for start in self._nodes:
            if start in visited:
                continue
            components += 1
            visited.add(start)
            queue = deque([start])
            while queue:
                current = queue.popleft()
                for neighbor in adjacency[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        return components

    def _has_directed_cycle(self) -> bool:
        """Pomocna metoda - provera ciklusa u usmerenom grafu (Kahn-ov algoritam)"""
        in_degree: Dict[str, int] = {node_id: 0 for node_id in self._nodes}
        successors: Dict[str, List[str]] = {node_id: [] for node_id in self._nodes}
        for edge in self._edges.values():
            in_degree[edge.target.id] += 1
            successors[edge.source.id].append(edge.target.id)

        queue = deque(node_id for node_id, degree in in_degree.items() if degree == 0)
        removed = 0
        while queue:
            current = queue.popleft()
            removed += 1
            for successor in successors[current]:
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)
        return removed < len(self._nodes)