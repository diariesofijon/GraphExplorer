#!/usr/bin/env python
# pylint: disable=C0103,W0622,E0001

'''
Drivers for loading graphs
'''

import abc
from dataclasses import dataclass, field


# TODO: realize the conception from base.py that would be work in singletone way
    # ids_map: Dict[str, list] = field(default_factory=lambda:{'A1.': [0]})
class IdsMapAbstract(abc.ABC):
    pass

class IdsMapBase(IdsMapAbstract):
    pass


class IdsMapTxt(IdsMapBase):
    pass

class IdsMapCsv(IdsMapBase):
    pass


class IdsMapYaml(IdsMapBase):
    pass
