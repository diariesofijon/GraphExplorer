#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

from lib import abc
from typing import TypeVar, Iterable, Set


# types
GE = TypeVar('GE', bound=abc.AbstractElement)
GM = TypeVar('GM', bound=abc.AbstractGraphMask)
GGE = Iterable[GE]
Chain = TypeVar('Chain', bound=abc.AbstractChain)
Tree = TypeVar('Tree', bound=abc.AbstractTree)
Loader = TypeVar('Loader', bound=abc.AbstractLoader)
NumericalSequence = Set[int]
ChainNumericals = Set[NumericalSequence]
