#!/usr/bin/env python3

import typing
import platform
import subprocess
import sys
import os


# -------------------------------
# VARIABLES DEFENITION
# -------------------------------

SYSTEM_INFO: typing.Dict = platform.freedesktop_os_release()
PATH: str                = os.environ.get('PATH', '')
PLATFORM: str            = sys.platform
KERNEL: str              = PLATFORM
NAME: str                = SYSTEM_INFO.get('NAME', '')
VERSION: str             = SYSTEM_INFO.get('VERSION', '')
VARIANT: str             = SYSTEM_INFO.get('VARIANT', '')
ID: str                  = SYSTEM_INFO.get('ID', '')
ID_LIKE: str             = SYSTEM_INFO.get('ID_LIKE', '')
VERSION_ID: str          = SYSTEM_INFO.get('VERSION_ID', '')
VARIANT_ID: str          = SYSTEM_INFO.get('VARIANT_ID', '')

# -------------------------------
# PREDICATS
# -------------------------------

LINUX_BASED: typing.Boolean = (PLATFORM is 'linux')
IS_UBUNTU: typing.Boolean = (NAME is 'ubuntu')

# -------------------------------
# ASSERTION TO INSPECT THE RIGHT ENVIRONMENT
# -------------------------------

assert LINUX_BASED

if LINUX_BASED:
    assert IS_UBUNTU

assert PATH