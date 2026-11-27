"""Testovi za parser upita filtera"""

import pytest

from sok.api import GraphError
from sok.core.exceptions import InvalidQueryError
from sok.core.filter_parser import COMPARATORS, FilterQuery, parse_filter


@pytest.mark.parametrize("operator", COMPARATORS)
def test_parse_every_comparator(operator):
    query = parse_filter(f"age {operator} 25")

    assert query == FilterQuery("age", operator, "25")


def test_parse_without_spaces():
    assert parse_filter("age>=25") == FilterQuery("age", ">=", "25")


def test_parse_ignores_extra_spaces():
    assert parse_filter("   age   <=   25   ") == FilterQuery("age", "<=", "25")


def test_two_character_comparator_is_recognized_before_one_character():
    query = parse_filter("age >= 25")

    assert query.operator == ">="
    assert query.value == "25"


def test_value_can_contain_spaces():
    assert parse_filter("name == Alice Smith") == FilterQuery("name", "==", "Alice Smith")


def test_value_stays_string():
    query = parse_filter("birth_date < 2000-05-17")

    assert query.value == "2000-05-17"
    assert isinstance(query.value, str)


@pytest.mark.parametrize("text", [
    "",
    "   ",
    "age",
    "age 25",
    "age = 25",
    "age => 25",
    "age >== 25",
    ">= 25",
    "age >=",
    "age >=   ",
    "first name == Tom",
])
def test_invalid_query_raises_error(text):
    with pytest.raises(InvalidQueryError):
        parse_filter(text)


def test_error_message_contains_query():
    with pytest.raises(InvalidQueryError, match="age = 25"):
        parse_filter("age = 25")


def test_invalid_query_error_is_graph_error():
    with pytest.raises(GraphError):
        parse_filter("age = 25")
