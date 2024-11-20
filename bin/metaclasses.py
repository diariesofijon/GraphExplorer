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

class MetaElement(type):
	pass

class MetaGraph(type):
	pass

class MetaTree(type):
	pass
