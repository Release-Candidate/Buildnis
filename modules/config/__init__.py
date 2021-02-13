# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

__all__ = ["Config", "PROJECT_FILE_NAME",
           "MODULE_FILE_NAME", "BUILD_FILE_NAME", "VERSION"]

import collections 

ConfigVersion = collections.namedtuple("Version", ["major", "minor"])
VERSION = ConfigVersion(major="1", minor="0")

PROJECT_FILE_NAME = "project_config"

MODULE_FILE_NAME = "module_config"

BUILD_FILE_NAME = "build_config"
