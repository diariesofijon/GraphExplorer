#!/usr/bin/env python

import config


'''
Have to manipulate dataclasses mechanism to make data structures easier to use.
First of all metaclass would be key tool to make whole composition. And also
should be based on abc classes
'''


# TODO: Inheritance deep of any MetaClass has no bigger 3 times


class MetaChain(type):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaChainException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


class MetaLoader(type):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaLoaderException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


class MetaTxtLoader(MetaLoader):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaLoaderException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


class MetaCsvLoader(MetaLoader):
	pass


class MetaYamlLoader(MetaLoader):
	pass


class MetaEisehowerLoader(MetaLoader):
	pass


class MetaElement(type):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaElementException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


class MetaRepresentativeElement(MetaElement):
	'''
 	The element is easier to show and easier to debugging. But the element
  	is harder to store in the memory.
 	'''


class MetaGraph(type):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaGraphException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


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


class MetaTree(type):
	
	def __new__(mls, cls, bases, attrs):
		if len(mro(mls)) > config.MetaClassIneritanceDepth:
			raise config.MetaTreeException(cls, bases, attrs)
		return type.__new__(mls, cls, bases, attrs)


class MetaAnalogGraph(MetaTree):
	'''
 	Produce analog graph's algorithms behavior strictly and will detect that
  	the graph has accepted existed logic or similar to base logic.
 	'''


class MetaFrozenTree(MetaTree):
	'''
	Tree has immutable and sized less than mutable.
 	'''
