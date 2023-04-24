#!/usr/bin/env python

import re
from dataclasses import dataclass
from typing import Optional


__all__ = (
    'StringRegularExpressionMaskAbstract', 'RepresentativeGraphElementAbstract')


@dataclass
class StringRegularExpressionMaskAbstract:

    def __repr__(self):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented


    def __new__(cls, *args, **kwargs):
        if not cls.tmp and not kwargs.get('tmp', ''):
            with open(cls.file, 'r') as file:
                cls.tmp = file.read()
        return super().__new__(cls, *args, **kwargs)

    @property
    def element_mask(self) -> Optional[str]:
        raise NotImplemented

    @property
    def node_mask(self) -> Optional[str]:
        raise NotImplemented

    @property
    def part_mask(self) -> Optional[str]:
        raise NotImplemented

    @property
    def tmp(self) -> Optional[str]:
        raise NotImplemented

    @property
    def separeter(self) -> Optional[str]:
        raise NotImplemented

    @property
    def file(self) -> str:
        raise NotImplemented

    @property
    def last_part(self) -> str:
        raise NotImplemented

    @property
    def element_class(self):
        raise NotImplemented

    def get_elements(self, part=None, id=None):
        raise NotImplemented

    def get_element(self, part=None, id=None):
        raise NotImplemented

    def _get_formated_links(self):
        raise NotImplemented

    @staticmethod
    def _get_ids(name):
        if len(tmp := name.split('-')) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

    def _convert_element(self, tmp, last_part):
        if  len((splited := tmp.split('.'))) == 1:
            splited = splited, ''
        ids, tmp = splited
        for id in self._get_ids(ids):
            grouped, body = tmp.split(':')
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body)
            yield data


@dataclass
class RepresentativeGraphElementAbstract:

    _children: list = None

    def __repr__(self):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented

    @property
    def id(self) -> str:
        raise NotImplemented

    @property
    def part(self) -> str:
        raise NotImplemented

    @property
    def grouped(self) -> str:
        raise NotImplemented

    @property
    def body(self) -> str:
        raise NotImplemented

    @property
    def graph(self):
        raise NotImplemented

    @property
    def children(self):
        if self._children is None:
            self._children = list(*self.graph.get_elements(
                part=self.part, id=self.id))
        return self._children

    @property
    def parents(self):
        for element in self.graph:
            for child in element.children:
                if int(child.id) == int(self.id):
                    yield element
                    break

    def load(self, string=None, part=None, id=None):
        if file:
            with open(self.graph.file, 'r') as file:
                return self.graph.get_element(part, id)
        elif string:
            return self.graph.get_element(part, id)
        else:
            raise Indexerror('Unexpected behavior')
