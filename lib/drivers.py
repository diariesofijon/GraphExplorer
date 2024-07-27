#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
Drivers for loading graphs
'''

from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict

import config
from lib import base, abc, shortcuts


class BaseLoader(abc.AbstractLoader):

    file_path: str = 'example'
    separeter: str = config.SEPARATES.get('NODE')
    element_class: abc.typing.GE = base.BaseElement

    _ids: FrozenSet = frozenset({})
    _map: Dict = {}

    def __init__(self, etype: abc.typing.GE = None):
        if etype:
            self.element_class: abc.typing.GE = etype
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

    file_path: str = config.FILE_DATA_LOADER_NAME

    # TODO: THAT IS NOT A GENERATOR
    def convert_element(self, tmp: str) -> abc.typing.GGE:
        ''' Engine convertor '''
        match len((splited:=tmp.split(':'))):
            case 0:
                grouped, body = 'splited', 'splited'
            case 1:
                grouped, body = splited, splited
            case _:
                grouped, body = splited
        for id in shortcuts.get_ids(ids):
        return self.element_class(
            id=index, grouped=grouped, body=body, graph=self)


class EisenhoverMatrixLoader(TxtLoader):

    def __init__(self, *args, **kwargs):
        self.ids_map: Dict[str, list] = {}
        super().__init__(*args, **kwargs)
        # TODO: Can't instantiate abstract class ... with abstract method ids_map
        # TODO: it has not work due exclude_tree ids_map has defrent logic
        # TODO: let's try makes it hardcode

    @property
    def whole_chain(self) -> Iterable:
        for link in super().whole_chain:
            if (tmp := link.strip()).endswith('.'):
                self.ids_map[tmp] += 1
                continue
            if tmp: # ATTENTION: ignore blank line
                yield from self.convert_element(tmp)

    def increase_maps_nums(self, line: str):
        part, indicator = shortcuts.eisenhower_part_spliter(str)
        self.whole_parts[str(part)] += self.increase_on

    def get_part_by_id(self, id: int):
        for part in self.ids_map.items():
            if self.ids_map[part] >= id:
                return part


class CsvLoader(BaseLoader):
    pass


class YamlLoader(BaseLoader):
    pass
