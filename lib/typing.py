#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

from typing import TypeVar, Iterable, Set
from lib import abc


# types
GE = TypeVar('GE', bound=abc.AbstractElement)
GM = TypeVar('GM', bound=abc.AbstractGraphMask)
GGE = Iterable[GE]
Chain = TypeVar('Chain', bound=abc.AbstractChain)
Tree = TypeVar('Tree', bound=abc.AbstractTree)
Loader = TypeVar('Loader', bound=abc.AbstractLoader)
Formatter = TypeVar('Formatter', bound=abc.AbstractTextFormatter)
NumericalSequence = Set[int]
ChainNumericals = Set[NumericalSequence]
