#!/usr/bin/env python
# pylint: disable=E0401

from typing import Iterable, Dict, Tuple, Callable

from bin import metaclasses

from lib import abc, shortcuts, typing

import config


class BaseChain(abc.AbstractChain):

    blank: bool = False

    def __init__(self, iterable: Iterable, *args, **kwargs):
        if self.blank:
            flambda: Callable[Iterable] = self.skip_blank
        else:
            flambda: Callable[Iterable] = self.store_blank
        super().__init__(filter(flambda, iterable), *args, **kwargs)

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

    blank: bool = False

    # TODO: add any logger to store whole collision
    def store_blank(self, element) -> bool:
        raise ValueError('Unexpected data')


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
        return True # TODO: just for debugging

    def store_blank(self, element) -> bool:
        part, indicator = shortcuts.eisenhower_part_spliter(element)
        self.whole_parts[str(part)] += self.increase_on
        return bool(indicator)
