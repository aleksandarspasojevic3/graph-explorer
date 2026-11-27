"""Filtriranje grafa"""

import operator
from datetime import date, datetime

from sok.api import AttributeValue, Graph

from .exceptions import InvalidQueryError
from .filter_parser import parse_filter

_COMPARE = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}


def filter_graph(graph: Graph, query: str) -> Graph:
    """
    Pravi podgraf cvorova ciji atribut zadovoljava filter, npr. "age >= 25"
    Vrednost iz upita se pretvara u tip atributa cvora, tekst se poredi bez obzira
    na velika i mala slova, a cvor bez atributa ne ulazi u rezultat

    :param graph: graf koji se filtrira
    :type graph: Graph
    :param query: upit oblika "<atribut> <komparator> <vrednost>"
    :type query: str
    :return: podgraf sa cvorovima koji zadovoljavaju filter i granama izmedju njih
    :rtype: Graph
    :raises InvalidQueryError: ako upit nije ispravan ili vrednost iz upita
        ne moze da se pretvori u tip atributa
    """
    parsed = parse_filter(query)
    compare = _COMPARE[parsed.operator]
    node_ids = []
    for node in graph.nodes:
        if not node.has_attribute(parsed.attribute):
            continue
        value = node.get_attribute(parsed.attribute)
        expected = _convert(parsed.value, value, parsed.attribute)
        if isinstance(value, str):
            value, expected = value.lower(), expected.lower()
        if compare(value, expected):
            node_ids.append(node.id)
    return graph.subgraph(node_ids)


def _convert(text: str, value: AttributeValue, attribute: str) -> AttributeValue:
    """Pomocna funkcija: pretvara vrednost iz upita u tip vrednosti atributa"""
    try:
        if isinstance(value, str):
            return text
        if isinstance(value, datetime):
            return datetime.fromisoformat(text)
        if isinstance(value, date):
            return date.fromisoformat(text)
        return type(value)(text)
    except ValueError:
        raise InvalidQueryError(
            f"Vrednost '{text}' nije ispravna za atribut '{attribute}' "
            f"tipa {type(value).__name__}.") from None
