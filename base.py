#!/usr/bin/env python

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class StringRegularExpressionMaskAbstract:
    
    element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = ''
    separeter: Optional[str] = '\n'
    file: str = 'graph_links.txt
    last_part: str = 'A1.'
    
    def __repr__(self):
        raise NotImplemented
    
    def __str__(self):
        raise NotImplemented
    
    @property
    def element_class(self):
        raise NotImplemented
    
    def get_elements(self, part=None, id=None):
        raise NotImplemented
        
    def get_element(self, part=None, id=None) -> RepresentativeGraphElement:
        raise NotImplemented

    def _get_formated_links(self):
        raise NotImplemented

    @staticmethod
    def _get_ids(name):
        if len(tmp := name.split('-')) == 2:
            return list(range(int(tmp[0]), int(tmp[1])+1))
        return [int(name)]

    def _convert_element(self, tmp, last_part):
        ids, tmp = tmp.split('.')
        for id in self._get_ids(ids):
            grouped, body = tmp.split(':')
            data = self.element_class(
                id=id, grouped=grouped, part=last_part, body=body)
            yield data
            
            
class StringByStringRegularExpressionMask(StringRegularExpressionMaskAbstract):
    
    def _get_formated_links(self):        
        for link in self.tmp.split('\n'):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            yield from self._convert_element(tmp, sel.flast_part)
            
@dataclass
class RepresentativeGraphElementAbstract:
    
    id: str = ''
    part: str = ''
    grouped: str = ''
    body: str = ''
    
    def __repr__(self):
        raise NotImplemented
    
    def __str__(self):
        raise NotImplemented
    
    @property
    def graph(self):
        raise NotImpolemented
    
    @property
    def children(self):
        return list(*self.graph.get_elements(
            part=self.part, id=self.id))
        
    def load(self, string=None, part=None, id=None):
        if file:
            with open(self.graph.file, 'r') as file:
                return self.graph.get_element(part, id)
        elif string:
            return self.graph.get_element(part, id)
        else:
            raise Indexerror('Unexpected behavior')
     
