# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     init.py
# Date:     18.Mar.2021
###############################################################################

from __future__ import annotations

import os
import pathlib
import sys

# Some useful paths.
tests_path = pathlib.Path(__file__).parent.absolute()
root_dir = os.path.normpath(tests_path.parent.absolute())
test_project_path = os.path.abspath("/".join([root_dir, "test_project"]))
sys.path.insert(0, root_dir)

# Path to the directory to write the generated configuration files to. Delete after the
# tests.
config_dir: str = "./delete_me"

# Some useful paths.
config_dir_abs = os.path.abspath("/".join([test_project_path, config_dir]))

# use that name to get the logger to use for the tests.
LOGGER_NAME = "tests_logger"
