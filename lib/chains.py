#!/usr/bin/env python
# pylint: disable=E0401

from typing import Iterable, Dict, Tuple, Callable

from bin import metaclasses
from lib import abc, shortcuts, typing
import config


class BaseChain(abc.AbstractChain):

    # TODO: reimagine conception to undo commented strings
    # blank: bool = False
    blank: bool = True

    def __init__(self, data: Optional[Iterable[T]] = None, unique: bool = True) -> None:
        # TODO: reimagine conception to undo commented strings
        # if self.blank:
        #     flambda: Callable[Iterable] = self.skip_blank
        # else:
        #     flambda: Callable[Iterable] = self.store_blank
        flambda = self.store_blank
        self._data: List[T] = list(data) if data else []
        if unique:
            # ensure uniqueness while preserving order
            seen = set()
            self._data = [x for x in self._data if not (x in seen or seen.add(x))]
        
        super().__init__(filter(flambda, iterable), *args, **kwargs)

    # --- Sequence API ---
    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    # --- Pythonic Dunders ---
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def __str__(self) -> str:
        return f"Chain(len={len(self)}, data={self._data})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AbstractChain) and self._data == other._data

    def __hash__(self) -> int:
        # Immutable representation for hashing
        return hash(tuple(self._data))

    def __sizeof__(self) -> int:
        # memory footprint of chain
        return super().__sizeof__() + sum(sys.getsizeof(x) for x in self._data)

    def __copy__(self) -> "AbstractChain[T]":
        return self.__class__(self._data)

    def __deepcopy__(self, memo) -> "AbstractChain[T]":
        import copy
        return self.__class__(copy.deepcopy(self._data, memo))

    # --- High-level Utilities ---
    def start(self, index: int = 0) -> T:
        """First element from index (default first element)."""
        return self._data[index]

    def end(self, index: int = 1) -> T:
        """Last element from offset (default last element)."""
        return self._data[-index]

    def filtered(self, func) -> typing.Chain:
        '''
        returns duplicated collection of filtered by the function
        due pythonic filter
        '''
        chain_class: typing.Chain = type(self)
        return chain_class(filter(func, self))

    def skip_blank(self, element) -> bool:
        return bool(element)

    def store_blank(self, element) -> bool:
        return bool(element)


class TxtChain(BaseChain):

    __metaclass__ = metaclasses.MetaChain

    # TODO: reimagine conception to undo commented strings
    # blank: bool = False
    blank: bool = True

    # TODO: reimagine conception to undo commented strings
    # TODO: add any logger to store whole collision
    # def store_blank(self, element) -> bool:
    #     raise ValueError('Unexpected data')

    # TODO: reimagine conception to undo commented strings
    # temporary code
    def store_blank(self, element) -> bool:
        part, indicator = shortcuts.eisenhower_part_spliter(element)
        self.whole_parts[str(part)] += self.increase_on
        return bool(indicator)



class GraphChain(TxtChain):

    _cache = None

    @property
    def cached_index_tuple(self) -> tuple:
        '''Should use as interable chain of indexes of children'''
        if self._cache:
            return self._cache

        last_chain, visited = [], self.deepest_chain
        for index, element in enumerate(visited):
            if index == (len(visited) - 1):
                break
            try:
                last_chain += element.children.idex(index+1)
            except ValueError:
                raise config.ThatIsNotGraph()
        self._cache = tuple(*last_chain)
        return self._cache

    @property
    def deepest_chain(self) -> TxtChain:
        '''All visited elements through dfs'''
        return GraphChain(self.graph.dfs()[1])

    @property
    def unconnected_chain(self) -> TxtChain:
        '''Whole queue of elements from dfs'''
        return GraphChain(self.graph.dfs()[0])


class EisenhowerMatrixChain(GraphChain):

    blank: bool       = True
    whole_parts: Dict = {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0}
    increase_on: int  = 1

    def skip_blank(self, element) -> bool:
        return not self.blank

    # TODO: reimagine conception to undo commented strings
    # def store_blank(self, element) -> bool:
    #     part, indicator = shortcuts.eisenhower_part_spliter(element)
    #     self.whole_parts[str(part)] += self.increase_on
    #     return bool(indicator)

class JSONChain(GraphChain):
    pass

