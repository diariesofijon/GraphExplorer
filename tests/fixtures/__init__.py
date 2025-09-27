#!/usr/bin/env python

from lib.drivers import BasicTextFormatter, TextGraphloader, Jsonloader
from lib.base import BaseGraphMask, CompositeMask

def from_text(text: str, formatter=None, loader=None, mask=None) -> BaseGraphMask:
    fmt = formatter if formatter is not None else BasicTextFormatter()
    ld = loader if loader is not None else TextGraphloader()
    formatted = fmt.format(text)
    graph_dict = ld.load(formatted)
    return BaseGraphMask(graph_dict, mask=mask)

def from_json(data: dict, loader=None, mask=None) -> BaseGraphMask:
    ld = loader if loader is not None else Jsonloader()
    graph_dict = ld.load(data)
    return BaseGraphMask(graph_dict, mask=mask)

def with_masks(*masks):
    if not masks:
        return None
    if len(masks) == 1:
        return masks[0]
    return CompositeMask(*masks)
