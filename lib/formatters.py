#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0622,E0001
# pylint: disable=E0401

from typing import Dict

import config
from lib import base, shortcuts, masks
from bin import protocols


class JSONFormatter(base.BasicTextFormatter):

    """
    A formatter for JSON-based graph data.
    Could later include JSON-specific serialization or validation.
    """

    indent: int = 2
    ensure_ascii: bool = False
	
	def get_kwargs_element(self, text: str) -> Dict:
		return {
			'id':		  None,
			'globals':	  None,
			'body':		  None,
			'graph':	  None,
			'chain_type': 'json',}

    def format(self, text: str) -> str:
        import json
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, indent=self.indent, ensure_ascii=self.ensure_ascii)
        except json.JSONDecodeError as decode_error:
            raise config.JSONError from decode_error
	
	def mask(self, kind: bool) -> protocols.MaskProtocol:
		return masks.NoMask()


class MatrixEisenhowerTXTFormatter(base.BasicTextFormatter):

	def format(self, text: str):
		return shortcuts.simplest_txt_element(text)

	def get_kwargs_element(self, text: str) -> Dict:
		return {
			'id':		  None,
			'globals':	  None,
			'part':		  None,
			'grouped':	  None,
			'body':		  None,
			'graph':	  None,
			'separeter':  None,
			'chain_type': None,}
