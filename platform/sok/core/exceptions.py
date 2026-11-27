"""Izuzeci platforme"""

from sok.api import GraphError


class InvalidQueryError(GraphError):
    """Upit za pretragu ili filter nije ispravan, ili vrednost iz upita
    ne moze da se pretvori u tip atributa"""
