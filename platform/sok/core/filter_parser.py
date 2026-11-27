"""Parser upita za filter"""

import re
from dataclasses import dataclass

from .exceptions import InvalidQueryError

COMPARATORS = ("==", "!=", ">=", "<=", ">", "<")
"""Dozvoljeni komparatori, dvoznakovni su prvi da se >= prepozna pre >"""

# atribut bez razmaka, komparator, vrednost koja ne pocinje znakom komparatora
_FILTER_PATTERN = re.compile(
    r"\s*(?P<attribute>[^\s=!<>]+)"
    r"\s*(?P<operator>==|!=|>=|<=|>|<)"
    r"\s*(?P<value>[^\s=!<>].*?)\s*")


@dataclass(frozen=True)
class FilterQuery:
    """
    Upit za filter podeljen na atribut, komparator i vrednost
    Vrednost ostaje string, u tip atributa je pretvara filter

    Primer::
        FilterQuery(attribute="age", operator=">=", value="25")
    """

    attribute: str
    operator: str
    value: str


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
