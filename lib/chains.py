#!/usr/bin/env python
# pylint: disable=E0401

from typing import Iterable, Dict, Tuple, Callable

from lib import abc, shortcuts, typing


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

    blank: bool = False

    # TODO: add any logger to store whole collision
    def store_blank(self, element) -> bool:
        raise ValueError('Unexpected data')


class EisenhowerMatrixChain(TxtChain):

    blank: bool       = True
    whole_parts: Dict = {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0}
    increase_on: int  = 1

    def skip_blank(self, element) -> bool:
        return True # TODO: just for debugging

    def store_blank(self, element) -> bool:
        part, indicator = shortcuts.eisenhower_part_spliter(element)
        self.whole_parts[str(part)] += self.increase_on
        return bool(indicator)
