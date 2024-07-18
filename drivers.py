#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
Drivers for loading graphs
'''

import abc
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict


# TODO: realize the conception from base.py that would be work in singletone way
# ids_map: Dict[str, list] = field(default_factory=lambda:{'A1.': [0]})
class IdsMapAbstract(abc.ABC):

    @property
    @abc.abstractmethod
    def whole_chain(self) -> Iterable:
        pass

    @abc.abstractmethod
    def convert_element(self, tmp: str):
        pass

class IdsMapBase(IdsMapAbstract):

    def _convert_element(self, tmp: str, last_part: GE) -> GGE:
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
        for id in self._get_ids(ids):
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body, graph=self)
            # TODO: just refactro it
            tmp = (self.ids_map.get(last_part, []) + [data])
            self.ids_map[last_part] = tmp
            yield data


class IdsMapTxt(IdsMapBase):

    def convert_element(self, tmp: str, last_part: GE) -> GGE:
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
        for id in self._get_ids(ids):
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body, graph=self)
            # TODO: just refactro it
            tmp = (self.ids_map.get(last_part, []) + [data])
            self.ids_map[last_part] = tmp
            yield data


    @staticmethod
    def get_ids(name: str) -> List[int]:
        ''' Clear function that implement name to ids '''
        if len((tmp := name.split('-'))) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

class IdsMapCsv(IdsMapBase):
    pass


class IdsMapYaml(IdsMapBase):
    pass
