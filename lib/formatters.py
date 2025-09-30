#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

import config
import base
import shortcuts


class MatrixEisenhowerTXTFormatter(base.BasicTextFormatter):

	def format(self, text: str):
		return shortcuts.simplest_txt_element(text)

	def get_kwargs_element(self, text: str) -> :
		return {
			'id':		  None,
			'globals':	  None,
			'part':		  None,
			'grouped':	  None,
			'body':		  None,
			'graph':	  None,
			'separeter':  None,
			'chain_type': None,}