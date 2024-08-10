#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

'''
Drivers for loading graphs
'''

from dataclasses import dataclass, field
from typing import (
    Optional, List, Union, Iterable, FrozenSet,
    Dict, Callable)

import config
from lib import base, abc, shortcuts, typing


class BaseLoader(abc.AbstractLoader):

    file_path: str = 'example'
    separeter: str = config.SEPARATES.get('NODE')
    element_class: typing.GE = base.BaseElement

    _ids: FrozenSet = frozenset({})
    _map: Dict = {}

    def __init__(self, etype: Optional[typing.GE] = None):
        if etype:
            self.element_class: typing.GE = etype
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

    def loads_from(self, path: str, mode: str='r', starts: int= 0):
        with open(path, mode, encoding=config.ENCODING) as file:
            self.cached_context: str = file.read()
        return self.cached_context[starts:]

    @property
    def whole_chain(self) -> Iterable:
        self.loads_from(self.file_path)
        separeted: Iterable = self.cached_context.split(self.separeter)
        yield from self.mapping_fuction(self.chain_mapping_fuction, separeted)

    # TODO: explain the idea in docs
    def mapping_fuction(self, func: Callable, sequence: Iterable):
        yield from map(func, sequence)

    # TODO: explain the idea in docs
    def chain_mapping_fuction(self, *args, **kwargs):
        return self.convert_element(*args, **kwargs)


class TxtLoader(BaseLoader):

    file_path: str = config.FILE_DATA_LOADER_NAME
    _last_index: int = 0


    # TODO: don't foget legace convert element and make the idea to
    # TODO: uneffectable deletion legace come true
    # def _convert_element(self, tmp: str, last_part: GE) -> GGE:
    #     ''' Engine convertor '''
    #     # shortcuts.eisenhower_part_spliter
    #     if len((splited := tmp.split('.'))) == 1:
    #         splited = splited[0], ''
    #     ids, tmp = splited
    #     match len((splited:=tmp.split(':'))):
    #         case 0:
    #             grouped, body = 'splited', 'splited'
    #         case 1:
    #             grouped, body = splited, splited
    #         case _:
    #             grouped, body = splited
    #     # shortcuts.get_ids
    #     for id in self._get_ids(ids):
    #         data = self.element_class(
    #             id=id, grouped=grouped, part=last_part, body=body, graph=self)
    #         # TODO: have to be strictly increased instead of redefining
    #         self.ids_map[last_part] = id
    #         yield data

    # TODO: THAT IS NOT A GENERATOR
    def convert_element(self, tmp: str) -> typing.GGE:
        ''' Engine convertor '''
        match len((splited:=tmp.split(':'))):
            case 0:
                grouped, body = 'splited', 'splited'
            case 1:
                grouped, body = splited, splited
            case _:
                grouped, body = splited
        self._last_index += 1
        return self.element_class(
            id=self._last_index, grouped=grouped, body=body, graph=self)


class EisenhoverMatrixLoader(TxtLoader):

    def __init__(self, *args, **kwargs):
        self.ids_map: Dict[str, list] = {}
        super().__init__(*args, **kwargs)
        # TODO: Can't instantiate abstract class ... with abstract method ids_map
        # TODO: it has not work due exclude_tree ids_map has defrent logic
        # TODO: let's try makes it hardcode

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


class CsvLoader(BaseLoader):
    pass


class YamlLoader(BaseLoader):
    pass
