#!/usr/bin/env python
# pylint: disable=C0103,W0622,E1136
# pylint: disable=E0401

# TODO: explaine the main idea of elements

from typing import Optional, List
from dataclasses import dataclass

from lib import base

@dataclass
class RepresentativeElement(base.BaseElement):

    ''' Sensetive turn off '''


    # TODO: move all show logic to new console or graphic interface in MIXIN
    # inheretince way
    def show_children(self):
        ''' Texted view of children of the elemenet '''
        return self._separeter().join(str(child) for child in self.children)

    def show_parents(self):
        ''' Texted view of parents of the elemenet '''
        return self._separeter().join(str(parent) for parent in self.parents)

    def walk(self, left: bool = True, chain: Optional[List] = None):
        '''
        Walking down through the graph to the deep to see how grap was changed
        '''
        if chain:
            index = chain.pop()
        else:
            # TODO: that's arise trouble because self is not iterable
            return self
        next_el = self.children[index] if left else self.children.end(index)
        yield next_el
        # fix: make deep searching algorithm based on this property
        yield from next_el.walk(left=left, chain=chain)