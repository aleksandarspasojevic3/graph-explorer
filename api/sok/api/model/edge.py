"""Grana grafa"""

from typing import Mapping, Optional

from .element import AttributeValue, GraphElement
from .node import Node


class Edge(GraphElement):
    """
    Grana izmedju dva cvora
    Grana uvek pamti source (odakle ide) i target (gde ide)
    Da li se smer postuje zavisi od grafa: u usmerenom grafu
    grana ide od source ka target,
    a u neusmerenom vazi u oba smera
    Dozvoljena je i petlja (source i target su isti cvor),
    kao i vise grana izmedju istih cvorova sa razlicitim id-jevima

    Primer::
        siblings = Edge("1", alice, tom, {"name": "Siblings"})
    """

    def __init__(self, edge_id: str, source: Node, target: Node,
                 attributes: Optional[Mapping[str, AttributeValue]] = None):
        """
        :param edge_id: jedinstveni id grane unutar grafa
        :type edge_id: str
        :param source: cvor iz kog grana polazi
        :type source: Node
        :param target: cvor u koji grana ulazi
        :type target: Node
        :param attributes: pocetni atributi grane
        :type attributes: Mapping[str, AttributeValue] | None
        :raises InvalidAttributeTypeError: ako neka vrednost nije dozvoljenog tipa
        """
        super().__init__(edge_id, attributes)
        self._source = source
        self._target = target

    @property
    def source(self) -> Node:
        """
        :return: cvor iz kog grana polazi
        :rtype: Node
        """
        return self._source

    @property
    def target(self) -> Node:
        """
        :return: cvor u koji grana ulazi
        :rtype: Node
        """
        return self._target

    def __repr__(self) -> str:
        """Tekstualni prikaz grane, npr. Edge(id='1', '1' -> '2', attributes={})"""
        return (f"Edge(id={self.id!r}, {self._source.id!r} -> {self._target.id!r}, "
                f"attributes={dict(self.attributes)!r})")