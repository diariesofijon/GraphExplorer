#!/usr/bin/env python

from protocol import Protocol
from typing import runtime_checkable, Iterable


@runtime_checkable
class ProtocolInfo(Protocol):
	pass

@runtime_checkable
class ProtocolRepresintation(Protocol):
	pass
