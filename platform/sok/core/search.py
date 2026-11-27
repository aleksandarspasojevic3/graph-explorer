"""Pretraga grafa"""

from sok.api import Graph, Node


def search(graph: Graph, query: str) -> Graph:
    """
    Pravi podgraf cvorova kod kojih naziv ili vrednost nekog atributa sadrzi upit
    Velika i mala slova se ne razlikuju, a brojevi i datumi se porede kao tekst
    Prazan upit (ili samo razmaci) vraca ceo graf

    :param graph: graf koji se pretrazuje
    :type graph: Graph
    :param query: tekst koji se trazi
    :type query: str
    :return: podgraf sa pronadjenim cvorovima i granama izmedju njih
    :rtype: Graph
    """
    if not query.strip():
        return graph.subgraph(node.id for node in graph.nodes)
    text = query.lower()
    return graph.subgraph(node.id for node in graph.nodes if _matches(node, text))


def _matches(node: Node, text: str) -> bool:
    """Pomocna funkcija: da li naziv ili vrednost nekog atributa cvora sadrzi tekst"""
    for name, value in node.attributes.items():
        if text in name.lower() or text in str(value).lower():
            return True
    return False
