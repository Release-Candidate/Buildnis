# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

__all__ = ["config"]

# Exit constants, constants passed to ´sys.exit´
EXT_OK = 0
"""No error"""

EXT_ERR_CMDLINE = 1
"""Error parsing command line"""

EXT_ERR_LD_FILE = 2
"""Error reading file"""

EXT_ERR_DIR = 3
"""Error, directory does not exist or is not a directory"""

EXT_ERR_WR_FILE = 4
"""Error writing to file"""

EXT_ERR_PYTH_VERS = 5
"""Error, Python version too old"""

EXT_ERR_IMP_MOD = 6
"""Error importing module"""

EXT_ERR_NOT_VLD = 7
"""Error, file is not a valid configuration"""
