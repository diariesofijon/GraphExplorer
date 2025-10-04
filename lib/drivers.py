#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

'''
Drivers for loading graphs
'''

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    Optional, List, Union, Iterable, FrozenSet,
    Dict, Callable)

import config
from bin import metaclasses
from lib import base, shortcuts, typing, chains
from elements import RepresentativeElement

# TODO: mugrate it to metaclasses
from typing import Dict, Type
from lib.protocols import ProtocolLoader, LoaderDetector


class MetaLoader(type):

    '''
        Metaclass that automatically registers loader classes
    into the FactoryLoader registry.
    '''

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace)
        if hasattr(cls, "extensions") and isinstance(getattr(cls, "extensions", None), (list, tuple)):
            FactoryLoader.register_loader(cls)
        return cls


class FactoryLoader(LoaderDetector, metaclass=MetaLoader):

    '''
        Central factory for all loaders, powered by MetaLoader.
    Subclasses auto-register based on their `extensions`.
    '''

    _registry: Dict[str, Type[ProtocolLoader]] = {}

    @classmethod
    def register_loader(cls, loader_cls: Type[ProtocolLoader]):
        for ext in loader_cls.extensions:
            cls._registry[ext.lower()] = loader_cls

    def detect_loader(self, path: str) -> ProtocolLoader:
        ext = path.split('.')[-1].lower()
        if ext not in self._registry:
            raise ValueError(f"No loader registered for extension: {ext}")
        return self._registry[ext]()

    def load(self, path: str, type: str = "r", mode: str = "r", starts: int = 0):
        loader = self.detect_loader(path)
        return loader.loads_from(path, type=type, mode=mode, starts=starts)


class MockLoader(base.BaseLoader):

    file_path: str           = ''
    element_class: typing.GE = RepresentativeElement
    chain_type               = chains.BaseChain

    def loads_from(self, path: str, mode: str='r', starts: int= 0):
        return []


class TxtLoader(base.BaseLoader):

    __metaclass__            = metaclasses.MetaTxtLoader

    file_path: str           = config.FILE_DATA_LOADER_NAME_TXT
    element_class: typing.GE = RepresentativeElement
    chain_type               = chains.TxtChain


class EisenhowerMatrixLoader(TxtLoader):

    __metaclass__          = metaclasses.MetaEisenhowerLoader

    ids_map: Dict[str,int] = {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0}
    chain_type             = chains.EisenhowerMatrixChain

    def mapping_fuction(self, func: Callable, sequence: Iterable):
        for line in sequence:
            if (tmp := line.strip()).endswith('.'):
                self.ids_map[tmp] += 1
                continue
            if tmp: # ATTENTION: ignore blank line
                ids, lines = shortcuts.eisenhower_part_spliter(tmp)
                yield from func(ids, lines)

    def chain_mapping_fuction(self, ids: int, lines: str):
        return self.yielded_convert_element(ids, lines)

    def get_part_by_id(self, id: int):
        for part in self.ids_map.items():
            if self.ids_map[part] >= id:
                return part

    def yielded_convert_element(self, ids: int, lines: str):
        '''
            Due Eisenhowers logic in the source text file can be plurar lines.
        And each element arised from each line have contains different increased id
        '''
        return (self.convert_element(lines) for _ in ids)


class CSVLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaCSVLoader


class YamlLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaYamlLoader


class JSONLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaJSONLoader

    @property
    def map(self):
        return self._map

    @property
    def ids(self):
        return self._ids

    @property
    def whole_chain(self) -> Iterable:
        yield from self.mapping_fuction(
            self.chain_mapping_fuction, json.dump(self.cached_context))

    def convert_element(self, tmp: tuple) -> typing.GGE:
        ''' Engine convertor '''
        name, children = tmp
        self._last_index += 1
        return self.element_class(graph=self.instance_graph,
            id=self._last_index, grouped=name, body=repr(tmp))

    # TODO: explain the idea in docs
    def mapping_fuction(self, func: Callable, sequence: Iterable):
        if not isinstance(sequence, dict):
            raise TypeError('sequence could be dicts')
        yield from map(func, sequence.copy())

    # TODO: explain the idea in docs
    def chain_mapping_fuction(self, sequence: Dict[str, str]):
        return self.convert_element(sequence.popitem())

