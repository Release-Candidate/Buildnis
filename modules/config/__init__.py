# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

__all__ = ["Config", "Host", "PROJECT_FILE_NAME",
           "MODULE_FILE_NAME", "BUILD_FILE_NAME", "HOST_FILE_NAME", "VERSION", 
           "WINDOWS_OS_STRING", "LINUX_OS_STRING", "OSX_OS_STRING", "AMD64_ARCH_STRING",
           "I86_ARCH_STRING"]

import collections 

ConfigVersion = collections.namedtuple("Version", ["major", "minor"])
VERSION = ConfigVersion(major="1", minor="0")

PROJECT_FILE_NAME = "project_config"

MODULE_FILE_NAME = "module_config"

BUILD_FILE_NAME = "build_config"

HOST_FILE_NAME = "host_config"

WINDOWS_OS_STRING = "Windows"

LINUX_OS_STRING = "Linux"

OSX_OS_STRING = "OSX"

AMD64_ARCH_STRING = "x64"

I86_ARCH_STRING = "x86"

FilePath = str
