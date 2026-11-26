"""Zajednicka osnova za cvorove i grane - id i tipizirani atributi"""

from datetime import date
from types import MappingProxyType
from typing import Dict, Mapping, Optional, Union

from .exceptions import AttributeNotFoundError

AttributeValue = Union[int, float, str, date]
"""Dozvoljeni tipovi vrednosti atributa
    Vrednost se cuva u svom tipu (broj kao broj, datum kao datum), a ne kao string,
    da bi filtriranje moglo da poredi vrednosti prema njihovom tipu
    datetime.datetime je podtip od date i takodje je dozvoljen
    bool nije dozvoljen"""

ALLOWED_ATTRIBUTE_TYPES = (int, float, str, date)
"""Tipovi koje model prihvata kao vrednosti atributa (za proveru sa isinstance)"""


class GraphElement:
    """Osnovna klasa za Node i Edge
    Element ima jedinstven id i recnik atributa cije su vrednosti tipa
    AttributeValue, dva elementa su jednaka ako su istog tipa i imaju isti id"""

    def __init__(self, element_id: str, attributes: Optional[Mapping[str, AttributeValue]] = None):
        """
        :param element_id: jedinstveni id elementa unutar grafa
        :type element_id: str
        :param attributes: pocetni atributi elementa, moze biti None (bez atributa)
        :type attributes: Mapping[str, AttributeValue] | None
        :raises InvalidAttributeTypeError: ako neka vrednost nije dozvoljenog tipa
        """
        self._id = element_id
        self._attributes: Dict[str, AttributeValue] = {}
        if attributes is not None:
            for name, value in attributes.items():
                self.set_attribute(name, value)

    @property
    def id(self) -> str:
        """
        :return: jedinstveni id elementa
        :rtype: str
        """
        return self._id

    @property
    def attributes(self) -> Mapping[str, AttributeValue]:
        """
        Vraca sve atribute elementa samo za citanje
        Za izmenu atributa koristiti set_attribute i remove_attribute

        :return: atributi elementa (naziv -> vrednost)
        :rtype: Mapping[str, AttributeValue]
        """
        return MappingProxyType(self._attributes)

    def has_attribute(self, name: str) -> bool:
        """
        :param name: naziv atributa
        :type name: str
        :return: True ako element ima atribut sa tim nazivom
        :rtype: bool
        """
        return name in self._attributes

    def get_attribute(self, name: str) -> AttributeValue:
        """
        :param name: naziv atributa
        :type name: str
        :return: vrednost atributa, u svom tipu
        :rtype: AttributeValue
        :raises AttributeNotFoundError: ako atribut ne postoji
        """
        if name not in self._attributes:
            raise AttributeNotFoundError(f"Element '{self._id}' nema atribut '{name}'.")
        return self._attributes[name]

    def set_attribute(self, name: str, value: AttributeValue) -> None:
        """
        Dodaje novi atribut ili menja vrednost postojećeg

        :param name: naziv atributa
        :type name: str
        :param value: nova vrednost (int, float, str ili date)
        :type value: AttributeValue
        :raises InvalidAttributeTypeError: ako vrednost nije dozvoljenog tipa
        """
        self._attributes[name] = value

    def remove_attribute(self, name: str) -> None:
        """
        :param name: naziv atributa koji se brise
        :type name: str
        :raises AttributeNotFoundError: ako atribut ne postoji
        """
        if name not in self._attributes:
            raise AttributeNotFoundError(f"Element '{self._id}' nema atribut '{name}'.")
        del self._attributes[name]

    def __eq__(self, other: object) -> bool:
        """
        Dva elementa su jednaka ako su istog tipa i imaju isti id
        Atributi se ne porede - cvor sa id-jem "1" je isti cvor bez obzira na vrednosti atributa
        """
        return type(self) is type(other) and self._id == other._id

    def __hash__(self) -> int:
        """Hash se racuna iz tipa i id-ja, u skladu sa __eq__,
         da bi element mogao biti u skupu ili kljuc recnika"""
        return hash((type(self), self._id))

    def __repr__(self) -> str:
        """Tekstualni prikaz za ispis i debagovanje, npr. Node(id='1', attributes={'name': 'Alice'})"""
        return f"{type(self).__name__}(id={self._id!r}, attributes={self._attributes!r})"