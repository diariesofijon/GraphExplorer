#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0622,E0001,E0401

'''
Drivers for loading graphs
'''

import json
import csv
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import (
    Optional, List, Union, Iterable, FrozenSet, Dict, Callable, Type
)

import config
from bin import metaclasses, protocols
from lib import base, shortcuts, typing, chains, formatters
from elements import RepresentativeElement


class FactoryLoader(protocols.LoaderDetector):

    """
    Central factory for all loaders, powered by MetaLoader.
    Subclasses auto-register based on their `extensions`.
    """

    __metaclass__ = metaclasses.MetaLoader

    _registry: Dict[str, Type["BaseLoader"]] = {}

    @classmethod
    def register_loader(cls, loader_cls: Type["BaseLoader"]):
        for ext in getattr(loader_cls, "extensions", []):
            cls._registry[ext.lower()] = loader_cls

    def detect_loader(self, path: str) -> "BaseLoader":
        ext = path.split('.')[-1].lower()
        if ext not in self._registry:
            raise ValueError(f"No loader registered for extension: {ext}")
        return self._registry[ext]()

    def load(self, path: str, type: str = "r", mode: str = "r", starts: int = 0):
        loader = self.detect_loader(path)
        return loader.loads_from(path, type=type, mode=mode, starts=starts)


@dataclass
class MockLoader(base.BaseLoader):

    file_path: str = ''
    element_class: typing.GE = RepresentativeElement
    chain_type = chains.BaseChain

    def loads_from(self, path: str, mode: str = 'r', starts: int = 0):
        return []


@dataclass
class TxtLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaTxtLoader

    file_path: str = config.FILE_DATA_LOADER_NAME_TXT
    element_class: typing.GE = RepresentativeElement
    chain_type = chains.TxtChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.MatrixEisenhowerTXTFormatter)


@dataclass
class EisenhowerMatrixLoader(TxtLoader):

    __metaclass__ = metaclasses.MetaEisenhowerLoader

    ids_map: Dict[str, int] = field(default_factory=lambda: {'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0})
    chain_type = chains.EisenhowerMatrixChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.MatrixEisenhowerTXTFormatter)

    def mapping_fuction(self, func: Callable, sequence: Iterable):
        for line in sequence:
            if (tmp := line.strip()).endswith('.'):
                self.ids_map[tmp] += 1
                continue
            if tmp:  # ignore blank line
                ids, lines = shortcuts.eisenhower_part_spliter(tmp)
                yield from func(ids, lines)

    def chain_mapping_fuction(self, ids: int, lines: str):
        return self.yielded_convert_element(ids, lines)

    def get_part_by_id(self, id: int):
        for part, count in self.ids_map.items():
            if count >= id:
                return part

    def yielded_convert_element(self, ids: int, lines: str):
        """Implements Eisenhower logic: each line has incremented id"""
        return (self.convert_element(lines) for _ in ids)


@dataclass
class CSVLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaCSVLoader

    extensions = ['csv', 'tsv']
    element_class = RepresentativeElement
    chain_type = chains.GraphChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.JSONFormatter)

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        with open(path, mode, encoding="utf-8") as f:
            return list(csv.reader(f))


@dataclass
class YamlLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaYamlLoader

    try:
        import yaml
        print(f'You have PyYAML {yaml.__version__}.')
    except ImportError:
        print('You cannot use this YamlLoader without PyYAML.\nTry: pip install pyyaml')

    extensions = ['yaml', 'yml']
    element_class = RepresentativeElement
    chain_type = chains.GraphChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.JSONFormatter)

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        with open(path, mode) as f:
            return self.yaml.safe_load(f)


@dataclass
class JSONLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaJSONLoader

    element_class = RepresentativeElement
    chain_type = chains.JSONChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.JSONFormatter)

    @property
    def map(self):
        return getattr(self, "_map", None)

    @property
    def ids(self):
        return getattr(self, "_ids", None)

    @property
    def whole_chain(self) -> Iterable:
        yield from self.mapping_fuction(
            self.chain_mapping_fuction, json.dump(self.cached_context))

    def convert_element(self, tmp: tuple) -> typing.GGE:
        """Convert JSON tuple to element."""
        name, children = tmp
        self._last_index += 1
        return self.element_class(
            graph=self.instance_graph,
            id=self._last_index,
            grouped=name,
            body=repr(tmp)
        )

    def mapping_fuction(self, func: Callable, sequence: Iterable):
        if not isinstance(sequence, dict):
            raise TypeError('sequence must be a dict')
        yield from map(func, sequence.copy())

    def chain_mapping_fuction(self, sequence: Dict[str, str]):
        return self.convert_element(sequence.popitem())


@dataclass
class XMLLoader(base.BaseLoader):

    __metaclass__ = metaclasses.MetaLoader

    extensions = ['xml', 'xsd']
    element_class = RepresentativeElement
    chain_type = chains.GraphChain
    formatter: base.BasicTextFormatter = field(default_factory=formatters.JSONFormatter)

    def loads_from(self, path: str, type: str, mode: str = "r", starts: int = 0):
        tree = ET.parse(path)
        return tree.getroot()
