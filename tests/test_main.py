# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     test_main.py
# Date:     18.Mar.2021
###############################################################################

from __future__ import annotations

import os
import pathlib
import runpy
import sys
from unittest import mock

import pytest


@pytest.mark.fast
def test_main() -> None:
    """Try to run program as Python 3.6."""
    test_project_path = pathlib.Path(__file__).parent.absolute()
    root_dir = os.path.normpath(test_project_path.parent.absolute())
    sys.path.insert(0, root_dir)

    with mock.patch.object(sys, "version_info") as mock_vers:
        mock_vers.major = 3
        mock_vers.minor = 6
        with pytest.raises(expected_exception=SystemExit) as excp:
            runpy.run_module("buildnis", run_name="__main__")
            assert excp.value.args[0] == 1  # nosec
