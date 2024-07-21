#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
Drivers for loading graphs
'''

import abc
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict
import config
import base
from data_structures import GraphTreeRepresentationMask


# TODO: realize the conception from base.py that would be work in singletone way
# ids_map: Dict[str, list] = field(default_factory=lambda:{'A1.': [0]})
class AbstractLoader(abc.ABC):

    cached_context: str = ''

    @property
    @abc.abstractmethod
    def whole_chain(self) -> Iterable:
        pass

    @property
    @abc.abstractmethod
    def element_class(self) -> base.GE:
        pass

    @property
    @abc.abstractmethod
    def ids(self) -> FrozenSet:
        pass

    @property
    @abc.abstractmethod
    def map(self) -> Dict:
        pass

    @abc.abstractmethod
    def loads_from(self, path: str, type: str, mode: str='r', starts: int= 0):
        pass

    @abc.abstractmethod
    def convert_element(self, tmp: str) -> base.GGE:
        pass


class BaseLoader(AbstractLoader):

    file_path: str = 'example'
    separeter: str = config.SEPARATES.get('NODE')
    element_class: base.GE = GraphTreeRepresentationMask

    _ids: FrozenSet = frozenset({})
    _map: Dict = {}

    def __init__(self, etype: base.GE = None):
        if etype:
            self.element_class: base.GE = etype
        self.loads_from(self.file_path)

    def __len__(self):
        return len(self.ids)

    @property
    def map(self):
        if not self._map:
            for idx, element in enumerate(self.whole_chain):
                self._map[idx+1] = element
        return self._map

    @property
    def ids(self):
        if not self._ids:
            self._ids = frozenset(map(int, self.map.keys()))
        return self._ids

    def loads_from(self, path: str, type: str= 'txt', mode: str='r', starts: int= 0):
        with open(path, mode, encoding=config.ENCODING) as file:
            self.cached_context: str = file.read()
        return self.cached_context[starts:]

    @property
    def whole_chain(self) -> Iterable:
        self.loads_from(self.file_path)
        separeted: Iterable = self.cached_context.split(self.separeter)
        yield from map(self.convert_element, separeted)


class TxtLoader(BaseLoader):

    file_path: str = 'output.txt'

    # TODO: THAT IS NOT A GENERATOR
    def convert_element(self, tmp: str) -> base.GGE:
        ''' Engine convertor '''
        if len((splited := tmp.split('.'))) == 1:
            splited = splited[0], ''
        ids, tmp = splited
        match len((splited:=tmp.split(':'))):
            case 0:
                grouped, body = 'splited', 'splited'
            case 1:
                grouped, body = splited, splited
            case _:
                grouped, body = splited
        for id in self.get_ids(ids):
            data = self.element_class(
                id=id, grouped=grouped, body=body, graph=self)
            yield data

    @staticmethod
    def get_ids(name: str) -> List[int]:
        ''' Clear function that implement name to ids '''
        if len((tmp := name.split('-'))) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]


class EisenhoverMatrixLoader(TxtLoader):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: Can't instantiate abstract class ... with abstract method ids_map
        # TODO: it has not work due exclude_tree ids_map has defrent logic
        # TODO: let's try makes it hardcode
        self.ids_map: Dict[str, list] = {}

    @property
    def whole_chain(self) -> Iterable:
        for link in super().whole_chain:
            if (tmp := link.strip()).endswith('.'):
                self.ids_map[tmp] += 1
                continue
            if tmp: # ATTENTION: ignore blank line
                yield from self.convert_element(tmp)

    def get_part_by_id(self, id: int):
        for part in self.ids_map.items():
            if self.ids_map[part] >= id:
                return part


class CsvLoader(BaseLoader):
    pass


class YamlLoader(BaseLoader):
    pass
