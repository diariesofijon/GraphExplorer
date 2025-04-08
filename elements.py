#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136
# pylint: disable=E0401

# TODO: explaine the main idea of elements

from typing import Optional, List
from dataclasses import dataclass, field

from bin import metaclasses
from lib import base, chains


__all__ = ('RepresentativeElement', 'EisenhowerElement')


@dataclass(frozen=True, kw_only=True, slots=True, unsafe_hash=True)
class RepresentativeElement(base.BaseElement):

    ''' Sensetive turn off '''

    __metaclass__ = metaclasses.MetaRepresentativeElement

    # TODO: move all show logic to new console or graphic interface in MIXIN
    # inheretince way
    def show_children(self):
        ''' Texted view of children of the elemenet '''
        return self.separater.join(str(child) for child in self.children)

    def show_parents(self):
        ''' Texted view of parents of the elemenet '''
        return self.separater.join(str(parent) for parent in self.parents)

    def walk(self, left: bool = True):
        '''
        Walking down through the graph to the deep to see how grap was changed
        '''
        if not self.children:
            yield self
        yield (next_el := self.children[0] if left else self.children[-1])
        yield from next_el.walk(left=left)

    def input_walk(self):
        '''
        Walking down through the graph to the deep to see how grap was changed
        But here you can chose which element of children you want ot pick
        Point that: works when interface is CLI!!!!
        '''
        # TODO: concept this cli to migrate it to the cli.py
        for index, child in enumerate(self.children):
            print('-'*20)
            print(f'index: {index}\ndata:\n{child}')
            print('\n\n')
        else:
            yield self
        if (index := int(input('type index:'))) in range(0,len(self.children)-1):
            yield (next_el := self.children[index])
            yield from next_el.input_walk()
        else:
            print('You have typed wrogn index', index, 'please, try again!')
            yield from self.input_walk()


@dataclass(frozen=True, kw_only=True, slots=True, unsafe_hash=True)
class EisenhowerElement(RepresentativeElement):

    part: str         = field(default='A')
    edges_based: bool = field(default=False)
    unconnected: bool = field(default=False)
    chain_type        = chains.EisenhowerMatrixChain
