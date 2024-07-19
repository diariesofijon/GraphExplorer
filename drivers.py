#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
Drivers for loading graphs
'''

import abc
from dataclasses import dataclass, field
from typing import Optional, List, Union, Iterable, FrozenSet, Dict
import config


# TODO: realize the conception from base.py that would be work in singletone way
# ids_map: Dict[str, list] = field(default_factory=lambda:{'A1.': [0]})
class IdsMapAbstract(abc.ABC):

    @property
    @abc.abstractmethod
    def whole_chain(self) -> Iterable:
        pass

    @property
    @abc.abstractmethod
    def element_class(self):
        pass

    @property
    @abc.abstractmethod
    def ids(self) -> Dict:
        pass

    @abc.abstractmethod
    def loads_from(self, path: str, type: str, mode: str='r', starts: int= 0):
        pass

    @abc.abstractmethod
    def convert_element(self, tmp: str):
        pass

class IdsMapBase(IdsMapAbstract):

    def loads_from(self, path: str, type: str= 'txt', mode: str='r', starts: int= 0):
        context: str = ''
        with open(path, mode, encoding=config.ENCODING) as file:
            context: str = file.read()
        return context[starts:]


class IdsMapTxt(IdsMapBase):

    separeter: str = config.SEPARATES.get('NODE')

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
        for id in self.get_ids(ids):
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body, graph=self)
        # TODO: just refactro it
        #     tmp = (self.ids_map.get(last_part, []) + [data])
        #     self.ids_map[last_part] = tmp
            yield data

    @staticmethod
    def get_ids(name: str) -> List[int]:
        ''' Clear function that implement name to ids '''
        if len((tmp := name.split('-'))) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

class EisenhoverMatrix(IdsMapTxt):

    def get_formated_links(self):
        for link in self.tmp.split(self.separeter):
            if (tmp := link.strip()).endswith('.'):
                last_part = tmp
                continue
            if not tmp:
                # ATTENTION: ignore blank line
                continue
            yield from self.convert_element(tmp, last_part)

    def get_part_by_id(self, id: int):


class IdsMapCsv(IdsMapBase):
    pass


class IdsMapYaml(IdsMapBase):
    pass
