#!/usr/bin/env python

import re
from dataclasses import dataclass
from typing import Optional

import base

@dataclass
class StringByStringRegularExpressionMask(base.StringRegularExpressionMaskAbstract):
    
    element_mask: Optional[str] = r'.+(?P<id>\D+)\..?(?P<grouped>.+): (?P<body>.*)\n'
    node_mask: Optional[str] = r'(?P<id>\D+)\((?P<children_list>.*)\)'
    part_mask: Optional[str] = r'.*(?P<id>\S+\D+\).\n'
    tmp: Optional[str] = ''
    separeter: Optional[str] = '\n'
    file: str = 'graph_links.txt
    last_part: str = 'A1.'
    
    def _get_formated_links(self):        
        for link in self.tmp.split('\n'):
            if (tmp := link.strip()).endswith('.'):
                self.last_part = tmp
                continue
            yield from self._convert_element(tmp, sel.flast_part)
