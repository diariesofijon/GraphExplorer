#!/usr/bin/env python
# pylint: disable=E0401,W0622,C0103,R0903

from typing import (
    Iterable, Dict, Tuple, Callable, Optional, List, TypeVar, Any, Iterator
)
from functools import reduce
import sys

from bin import metaclasses
from lib import abc, shortcuts, typing
import config


Callback = Optional[Callable[[Any], Any]]
E = TypeVar('E')


class BaseChain(abc.AbstractChain):
    """
    BaseChain implements a list-like and iterator-compatible collection
    with lazy functional behavior (map, filter, reduce). All operations
    are based on the iterator engine: __iter__ and __next__.
    """

    blank: bool = True
    unique: bool = False

    def __init__(
        self,
        data: Optional[Iterable[E]] = None,
        unique: bool = True,
        flambda: Callback = None,
    ):
        self._index = 0
        flambda = self.flambda if not flambda else flambda
        iterable = list(data) if data else []

        if unique or self.unique:
            seen = set()
            iterable = [x for x in iterable if not (x in seen or seen.add(x))]

        if flambda:
            iterable = list(filter(flambda, iterable))

        self._data: List[E] = iterable

    # --- Iterator Engine ---
    def __iter__(self) -> Iterator[E]:
        """Return iterator over chain data."""
        self._index = 0
        return self

    def __next__(self) -> E:
        """Next element from internal list."""
        if self._index >= len(self._data):
            raise StopIteration
        item = self._data[self._index]
        self._index += 1
        return item

    # --- Functional Methods built over iterator ---
    def __map__(self, func: Callable[[E], Any]) -> "BaseChain":
        """Return a new BaseChain lazily mapped over iterator."""
        def generator():
            for x in self:
                yield func(x)
        return self.__class__(generator())

    def __filter__(self, func: Callable[[E], bool]) -> "BaseChain":
        """Return a new BaseChain lazily filtered over iterator."""
        def generator():
            for x in self:
                if func(x):
                    yield x
        return self.__class__(generator())

    def __reduce__(self, func: Callable[[Any, E], Any], initializer: Optional[Any] = None) -> Any:
        """Reduce the iterator stream into a single value."""
        iterator = iter(self)
        if initializer is not None:
            return reduce(func, iterator, initializer)
        return reduce(func, iterator)

    # --- Pythonic Behavior ---
    def __getitem__(self, index: int) -> E:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self._data)!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseChain) and list(self._data) == list(other._data)

    def __hash__(self) -> int:
        return hash(tuple(self._data))

    def __copy__(self) -> "BaseChain":
        return self.__class__(self._data)

    def __deepcopy__(self, memo) -> "BaseChain":
        import copy
        return self.__class__(copy.deepcopy(self._data, memo))

    def __sizeof__(self) -> int:
        return super().__sizeof__() + sum(sys.getsizeof(x) for x in self._data)

    # --- High-level Utilities ---
    def start(self, index: int = 0) -> E:
        return self._data[index]

    def end(self, index: int = 1) -> E:
        return self._data[-index]

    def filtered(self, func: Callable[[E], bool]) -> "BaseChain":
        """Return a filtered chain."""
        return self.__class__(filter(func, self._data))

    def skip_blank(self, element) -> bool:
        return bool(element)

    def store_blank(self, element) -> bool:
        return bool(element)


class TxtChain(BaseChain):
    """Works only with TxtLoader or text from RAM."""
    __metaclass__ = metaclasses.MetaChain
    blank: bool = True

    def store_blank(self, element) -> bool:
        part, indicator = shortcuts.eisenhower_part_spliter(element)
        self.whole_parts[str(part)] += self.increase_on
        return bool(indicator)


class GraphChain(TxtChain):
    """Graph-based traversal chain with cached dfs/bfs-based structure."""
    _cache: Optional[Tuple] = None

    @property
    def cached_index_tuple(self) -> tuple:
        if self._cache:
            return self._cache

        last_chain: List[E] = []
        visited: typing.Chain = self.deepest_chain
        for index, element in enumerate(visited):
            try:
                last_chain += element.children.index(index + 1)
            except ValueError:
                raise config.ThatIsNotGraph()
        self._cache = tuple(last_chain)
        return self._cache

    @property
    def deepest_chain(self) -> TxtChain:
        return GraphChain(self.graph.dfs()[1])

    @property
    def unconnected_chain(self) -> TxtChain:
        return GraphChain(self.graph.dfs()[0])


class EisenhowerMatrixChain(GraphChain):
    """Structured matrix chain for Eisenhower-style task prioritization."""

    blank: bool = True
    whole_parts: Dict = {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0}
    increase_on: int = 1

    def skip_blank(self, element) -> bool:
        return not self.blank


class JSONChain(GraphChain):
    """Simple graph chain based on JSON-like sources."""
    pass
