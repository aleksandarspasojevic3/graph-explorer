"""Izuzeci platforme
Nasledjuju GraphError iz modela, pa ih pozivalac (web, CLI) hvata
zajedno sa greskama modela i korisniku prikazuje poruku"""

from sok.api import GraphError


class InvalidQueryError(GraphError):
    """Upit za pretragu ili filter nije ispravan
    Baca se kada upit nije u ocekivanom obliku ili kada vrednost iz upita
    ne moze da se pretvori u tip atributa"""
