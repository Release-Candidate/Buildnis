# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     setup_teardown.py
# Date:     19.Mar.2021
###############################################################################

from __future__ import annotations

import logging
import os
import sys
import tempfile

import pytest

import tests


################################################################################
@pytest.fixture(scope="session")
def test_logger() -> None:
    """Set the logger to log to the `config_dir`."""
    ret_val = logging.getLogger(tests.LOGGER_NAME)
    ret_val.setLevel(logging.DEBUG)

    stdout_hdl = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(message)s")
    stdout_hdl.setFormatter(formatter)
    stdout_hdl.addFilter(lambda lvl: lvl.levelno < logging.ERROR)
    stdout_hdl.setLevel(logging.DEBUG)
    ret_val.addHandler(stdout_hdl)

    stderr_hdl = logging.StreamHandler(sys.stderr)
    err_formatter = logging.Formatter("%(levelname)s: %(message)s")
    stderr_hdl.setFormatter(err_formatter)
    stderr_hdl.setLevel(logging.ERROR)
    ret_val.addHandler(stderr_hdl)

    log_file_dir = tempfile.TemporaryDirectory(dir=tests.test_project_path)
    logfile = os.path.abspath("/".join([log_file_dir.name, "logfile.log"]))
    file_hdl = logging.FileHandler(logfile, mode="w")
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
    )
    file_hdl.setFormatter(file_formatter)
    file_hdl.setLevel(logging.DEBUG)
    ret_val.addHandler(file_hdl)

    print(log_file_dir.name)

    yield ret_val

    # teardown part

    logging.shutdown()
