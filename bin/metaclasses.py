#!/usr/bin/env python

import config
import lib


'''
Have to manipulate dataclasses mechanism to make data structures easier to use.
First of all metaclass would be key tool to make whole composition.
'''


__all__ = ('MetaChain', 'MetaLoader', 'MetaTxtLoader', 'MetaCsvLoader',
    'MetaYamlLoader', 'MetaEisehowerLoader', 'MetaElement', 'MetaGraph',
    'MetaRepresentativeGraph', 'MetaRepresentativeElement', 'MetaAnalogGraph',
    'MetaTree', 'MetaAnalogTree', 'MetaFrozenTree', 'MetaConfig')


# TODO: Inheritance deep of any MetaClass has no bigger 3 times
class MetaConfig(type):

    def __init_subclass__(mcs):
        if len(mcs.__mro__) > config.META_CLASS_INHERITANCE_DEPTH:
            raise config.MetaMroError(mcs)


class MetaChain(MetaConfig):

    existed: list[set] = []

    def __new__(mcs, cls, bases, attrs):
        if (content := set(attrs['iterable'])):
            if content in mcs.existed:
                raise config.MetaChain({
                'existed': 'chain has already arised with this order o eleements',})
            mcs.existed.append(content)
        attrs['existed'] = mcs.existed
        return MetaConfig.__new__(mcs, cls, bases, attrs)


class MetaLoader(MetaConfig):
    pass


class MetaTxtLoader(MetaLoader):
    pass


class MetaCsvLoader(MetaLoader):
    pass


class MetaYamlLoader(MetaLoader):
    pass


class MetaEisehowerLoader(MetaLoader):
    pass


class MetaElement(MetaConfig):
    pass


class MetaRepresentativeElement(MetaElement):
    '''
    The element is easier to show and easier to debugging. But the element
    is harder to store in the memory.
    '''


class MetaGraph(MetaConfig):

    # detect meta data from the source to clearly understand what should do for
    # each element
    story: dict[lib.typing.GM, dict] = {}

    def __new__(mcs, cls, bases, attrs):
        graph = MetaConfig.__new__(mcs, cls, bases, attrs)
        mcs.story[graph] = {'attrs': attrs}
        return graph


class MetaRepresentativeGraph(MetaGraph):
    '''
    The graph is easier to show and easier to debugging. But the graph
    is harder to store in the memory.
    '''


class MetaAnalogGraph(MetaGraph):
    '''
    Produce analog graph's algorithms behavior strictly and will detect that
    the graph has accepted existed logic or similar to base logic.
    '''


class MetaTree(MetaConfig):
    pass


class MetaAnalogTree(MetaTree):
    '''
    Produce analog graph's algorithms behavior strictly and will detect that
    the graph has accepted existed logic or similar to base logic.
    '''


class MetaFrozenTree(MetaTree):
    '''
    Tree has immutable and sized less than mutable.
    '''


# TODO: Let's check mro through assertion here!!!

assert config.META_CLASS_INHERITANCE_DEPTH
