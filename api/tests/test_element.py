"""Testovi za cvorove i grane: id, atributi, tipovi vrednosti i jednakost"""

from datetime import date, datetime

import pytest

from sok.api import AttributeNotFoundError, Edge, InvalidAttributeTypeError, Node


def test_node_has_id_and_attributes():
    node = Node("1", {"name": "Alice", "age": 25})

    assert node.id == "1"
    assert node.get_attribute("name") == "Alice"
    assert node.get_attribute("age") == 25


def test_node_without_attributes_has_empty_attributes():
    node = Node("1")

    assert dict(node.attributes) == {}


def test_nodes_do_not_share_attributes():
    first = Node("1")
    second = Node("2")

    first.set_attribute("x", 5)

    assert not second.has_attribute("x")


@pytest.mark.parametrize("value", [25, 1.65, "Alice", date(2000, 5, 17), datetime(2000, 5, 17, 10, 30)])
def test_allowed_types_are_kept_in_their_type(value):
    node = Node("1", {"value": value})

    assert node.get_attribute("value") == value
    assert type(node.get_attribute("value")) is type(value)


@pytest.mark.parametrize("value", [True, None, [1, 2], {"a": 1}, (1, 2)])
def test_set_attribute_rejects_invalid_types(value):
    node = Node("1")

    with pytest.raises(InvalidAttributeTypeError):
        node.set_attribute("value", value)


def test_constructor_rejects_invalid_types():
    with pytest.raises(InvalidAttributeTypeError):
        Node("1", {"active": True})


def test_set_attribute_changes_existing_value():
    node = Node("1", {"age": 25})

    node.set_attribute("age", 26)

    assert node.get_attribute("age") == 26


def test_get_missing_attribute_raises():
    node = Node("1")

    with pytest.raises(AttributeNotFoundError):
        node.get_attribute("age")


def test_remove_attribute():
    node = Node("1", {"age": 25})

    node.remove_attribute("age")

    assert not node.has_attribute("age")


def test_remove_missing_attribute_raises():
    with pytest.raises(AttributeNotFoundError):
        Node("1").remove_attribute("age")


def test_attributes_are_read_only():
    node = Node("1", {"age": 25})

    with pytest.raises(TypeError):
        node.attributes["age"] = 30


def test_id_cannot_be_changed():
    node = Node("1")

    with pytest.raises(AttributeError):
        node.id = "2"


def test_nodes_with_same_id_are_equal():
    assert Node("1", {"name": "Alice"}) == Node("1", {"name": "Bob"})
    assert Node("1") != Node("2")
    assert len({Node("1"), Node("1"), Node("2")}) == 2


def test_node_and_edge_with_same_id_are_not_equal():
    a, b = Node("A"), Node("B")

    assert Node("1") != Edge("1", a, b)


def test_edge_has_source_target_and_attributes():
    alice, tom = Node("1"), Node("2")

    edge = Edge("10", alice, tom, {"relation": "friends"})

    assert edge.id == "10"
    assert edge.source is alice
    assert edge.target is tom
    assert edge.get_attribute("relation") == "friends"


def test_edge_rejects_invalid_attribute_type():
    with pytest.raises(InvalidAttributeTypeError):
        Edge("10", Node("1"), Node("2"), {"weight": None})