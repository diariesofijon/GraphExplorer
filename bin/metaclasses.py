#!/usr/bin/env python

'''
Have to manipulate dataclasses mechanism to make data structures easier to use.
First of all metaclass would be key tool to make whole composition. And also
should be based on abc classes
'''

class MetaChain(type):
	pass


class MetaLoader(type):
	pass


class MetaTxtLoader(MetaLoader):
	pass


class MetaCsvLoader(MetaLoader):
	pass


class MetaYamlLoader(MetaLoader):
	pass


class MetaEisehowerLoader(MetaLoader):
	pass


class MetaElement(type):
	pass


class MetaRepresentativeElement(MetaElement):
	'''
 	The element is easier to show and easier to debugging. But the element
  	is harder to store in the memory.
 	'''


class MetaGraph(type):
	pass


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
	pass


class MetaAnalogGraph(MetaTree):
	'''
 	Produce analog graph's algorithms behavior strictly and will detect that
  	the graph has accepted existed logic or similar to base logic.
 	'''


class MetaFrozenTree(MetaTree):
	'''
	Tree has immutable and sized less than mutable.
 	'''

