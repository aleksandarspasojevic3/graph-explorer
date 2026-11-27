"""Parser upita za filtriranje grafa

Upit je oblika "<atribut> <komparator> <vrednost>", npr. "age >= 25"
Razmaci oko komparatora nisu obavezni ("age>=25"), a vrednost moze
sadrzati razmake ("name == Alice Smith")

Parser samo deli tekst na tri dela, vrednost ostaje string
Pretvaranje vrednosti u tip atributa radi filter, jer tek on zna kog je
tipa atribut cvora
"""

import re
from dataclasses import dataclass

from .exceptions import InvalidQueryError

COMPARATORS = ("==", "!=", ">=", "<=", ">", "<")
"""Dozvoljeni komparatori
Dvoznakovni su ispred jednoznakovnih, da bi se >= prepoznao pre >"""

_FILTER_PATTERN = re.compile(
    r"\s*(?P<attribute>[^\s=!<>]+)"
    r"\s*(?P<operator>==|!=|>=|<=|>|<)"
    r"\s*(?P<value>[^\s=!<>].*?)\s*")
"""Regularni izraz za upit filtera:
    attribute - naziv atributa, bez razmaka i znakova komparatora
    operator - jedan od komparatora, dvoznakovni se proveravaju prvi
    value - sve do kraja upita, ne sme poceti znakom komparatora
    (tako se "age >== 25" odbija umesto da vrednost bude "= 25")
Razmaci na pocetku, oko komparatora i na kraju se zanemaruju"""


@dataclass(frozen=True)
class FilterQuery:
    """
    Rezultat parsiranja upita za filter
    Objekat se ne moze menjati posle pravljenja (frozen)

    Primer::
        FilterQuery(attribute="age", operator=">=", value="25")
    """

    attribute: str
    """naziv atributa cvora, npr. age"""

    operator: str
    """komparator, jedan od COMPARATORS"""

    value: str
    """vrednost iz upita kao string, npr. 25"""


def parse_filter(query: str) -> FilterQuery:
    """
    Deli upit za filter na atribut, komparator i vrednost

    :param query: upit oblika "<atribut> <komparator> <vrednost>", npr. "age >= 25"
    :type query: str
    :return: atribut, komparator i vrednost iz upita
    :rtype: FilterQuery
    :raises InvalidQueryError: ako upit nije u ocekivanom obliku
    """
    match = _FILTER_PATTERN.fullmatch(query)
    if match is None:
        raise InvalidQueryError(
            f"Neispravan upit '{query}'. Ocekivan oblik je '<atribut> <komparator> <vrednost>', "
            f"komparatori su {', '.join(COMPARATORS)}.")
    return FilterQuery(match.group("attribute"), match.group("operator"), match.group("value"))
