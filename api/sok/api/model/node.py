"""Cvor grafa"""

from typing import Mapping, Optional

from .element import AttributeValue, GraphElement


class Node(GraphElement):
    """
    Cvor grafa
    Cvor ima jedinstven id i atribute
    Sam cvor ne zna sa kojim je granama povezan,
    to zna graf (Graph.edges_of, Graph.neighbors)

    Primer:
      alice = Node("1", {"name": "Alice", "age": 25})
    """

    def __init__(self, node_id: str, attributes: Optional[Mapping[str, AttributeValue]] = None):
        """
        :param node_id: jedinstveni id čvora unutar grafa
        :type node_id: str
        :param attributes: pocetni atributi cvora
        :type attributes: Mapping[str, AttributeValue] | None
        :raises InvalidAttributeTypeError: ako neka vrednost nije dozvoljenog tipa
        """
        raise NotImplementedError