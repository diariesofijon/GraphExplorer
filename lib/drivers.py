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
from lib import base, shortcuts, typing
from elements import RepresentativeElement


class TxtLoader(base.BaseLoader):

    file_path: str           = config.FILE_DATA_LOADER_NAME_TXT
    element_class: typing.GE = RepresentativeElement

    _last_index: int = 0

    # TODO: THAT IS NOT A GENERATOR
    def convert_element(self, tmp: str) -> typing.GGE:
        ''' Engine convertor '''
        grouped, body = shortcuts.separete_from_text_element(tmp)
        self._last_index += 1
        return self.element_class(
            id=self._last_index, grouped=grouped, body=body, graph=self)


@dataclass
class EisenhoverMatrixLoader(TxtLoader):

    ids_map: Dict[str,int] = field(default={'A1.': 0, 'B2.': 0, 'C3.': 0, 'L4.': 0})

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


class CsvLoader(base.BaseLoader):
    pass


class YamlLoader(base.BaseLoader):
    pass
