"""Zajednicka osnova za cvorove i grane - id i tipizirani atributi"""

from datetime import date
from typing import Mapping, Optional, Union

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
        raise NotImplementedError

    @property
    def id(self) -> str:
        """
        :return: jedinstveni id elementa
        :rtype: str
        """
        raise NotImplementedError

    @property
    def attributes(self) -> Mapping[str, AttributeValue]:
        """
        Vraca sve atribute elementa samo za citanje
        Za izmenu atributa koristiti set_attribute i remove_attribute

        :return: atributi elementa (naziv -> vrednost)
        :rtype: Mapping[str, AttributeValue]
        """
        raise NotImplementedError

    def has_attribute(self, name: str) -> bool:
        """
        :param name: naziv atributa
        :type name: str
        :return: True ako element ima atribut sa tim nazivom
        :rtype: bool
        """
        raise NotImplementedError

    def get_attribute(self, name: str) -> AttributeValue:
        """
        :param name: naziv atributa
        :type name: str
        :return: vrednost atributa, u svom tipu
        :rtype: AttributeValue
        :raises AttributeNotFoundError: ako atribut ne postoji
        """
        raise NotImplementedError

    def set_attribute(self, name: str, value: AttributeValue) -> None:
        """
        Dodaje novi atribut ili menja vrednost postojećeg

        :param name: naziv atributa
        :type name: str
        :param value: nova vrednost (int, float, str ili date)
        :type value: AttributeValue
        :raises InvalidAttributeTypeError: ako vrednost nije dozvoljenog tipa
        """
        raise NotImplementedError

    def remove_attribute(self, name: str) -> None:
        """
        :param name: naziv atributa koji se brise
        :type name: str
        :raises AttributeNotFoundError: ako atribut ne postoji
        """
        raise NotImplementedError