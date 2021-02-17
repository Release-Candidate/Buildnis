# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

__all__ = ["Config", "Host", "Check", "PROJECT_FILE_NAME",
           "MODULE_FILE_NAME", "BUILD_FILE_NAME", "HOST_FILE_NAME", "VERSION", 
           "WINDOWS_OS_STRING", "LINUX_OS_STRING", "OSX_OS_STRING", "AMD64_ARCH_STRING",
           "I86_ARCH_STRING", "CONFIGURE_SCRIPTS_PATH", "BUILD_TOOL_CONFIG_NAME"]

import collections 

# Types to use for type hints

ConfigVersion = collections.namedtuple("Version", ["major", "minor"])
VERSION = ConfigVersion(major="1", minor="0")

FilePath = str

OSName = str

Arch = str


# Constants to use for JSON files, arguments, ...

PROJECT_FILE_NAME = "project_config"

MODULE_FILE_NAME = "module_config"

BUILD_FILE_NAME = "build_config"

HOST_FILE_NAME = "host_config"

WINDOWS_OS_STRING = "Windows"

LINUX_OS_STRING = "Linux"

OSX_OS_STRING = "OSX"

AMD64_ARCH_STRING = "x64"

I86_ARCH_STRING = "x86"

CONFIGURE_SCRIPTS_PATH = "./configure_scripts"

BUILD_TOOL_CONFIG_NAME = "build_tool_config"
