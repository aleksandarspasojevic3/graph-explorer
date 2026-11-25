"""Izuzeci koje baca model grafa
Svi izuzeci nasledjuju GraphError, pa ih pozivalac (platforma, CLI, web)
moze uhvatiti zajedno i korisniku prikazati razumljivu poruku"""


class GraphError(Exception):
    """Osnovna klasa za sve greske modela grafa"""


class NodeNotFoundError(GraphError):
    """Cvor sa trazenim id-jem ne postoji u grafu"""


class EdgeNotFoundError(GraphError):
    """Grana sa trazenim id-jem ne postoji u grafu"""


class DuplicateNodeError(GraphError):
    """U grafu vec postoji cvor sa istim id-jem"""


class DuplicateEdgeError(GraphError):
    """U grafu vec postoji grana sa istim id-jem"""


class NodeHasEdgesError(GraphError):
    """Cvor ne moze da se obrise jer je povezan bar jednom granom
    Pre brisanja cvora moraju se obrisati sve grane sa kojima je povezan"""


class AttributeNotFoundError(GraphError):
    """Cvor ili grana nema atribut sa trazenim nazivom"""


class InvalidAttributeTypeError(GraphError):
    """Vrednost atributa nije dozvoljenog tipa (int, float, str ili date)"""