# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     test_project.py
# Date:     16.Mar.2021
###############################################################################

from __future__ import annotations

import os
import pathlib
import platform
import runpy
import sys
from typing import List

import pathvalidate
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st


################################################################################
def runBuildnis(cmd_line_args: List[str]) -> None:
    """Run the program with the given arguments.

    Returns the output of the command in the tuple `stdout, stderr`. The first element
    of the tuple holds the process' output on `stdout`, the second the output on
    `stderr`.

    Args:
        cmd_line_args (List[str]): The arguments to pass to `buildnis`.
    """
    test_project_path = pathlib.Path(__file__).parent.absolute()
    root_dir = os.path.normpath(test_project_path.parent.absolute())
    sys.path.insert(0, root_dir)

    sys_argv_list = [""]
    sys_argv_list.extend(cmd_line_args)
    sys_argv_list.append("./test_project/project_config.json")
    sys.argv = sys_argv_list

    runpy.run_module("buildnis", run_name="__main__")


################################################################################
def test_runVersion() -> None:
    """Run `buildnis` with the argument `--version` to show the version information."""
    try:
        runBuildnis(["--version"])
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec


################################################################################
def test_runHelp() -> None:
    """Run `buildnis` with the argument `--help` to show the usage information."""
    try:
        runBuildnis(["--help"])
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec


################################################################################
@settings(max_examples=5, deadline=None)
@given(
    arg=st.sampled_from(elements=["-q", "", "-v", "-vv"]), conf_out=st.text(max_size=20)
)
def test_runFirstTime(arg: str, conf_out: str) -> None:
    """Run Buildnis for the first time.

    Args:
        arg (str): The verbosity argument.
        conf_out (str): The path to the generated configuration directory.
    """
    try:
        arg_list = []
        if arg != "":
            arg_list.append(arg)
        if conf_out != "":
            sanitizePath(conf_out, arg_list)

        runBuildnis(arg_list)
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec


################################################################################
def sanitizePath(conf_out, arg_list) -> None:
    """Sanitize the given path `conf_out`, we want random paths, but not invalid ones.

    Args:
        conf_out ([type]): The path to sanitize.
        arg_list ([type]): The list to append the sanitized path to.
    """
    sanitized_conf = pathvalidate.sanitize_filename(conf_out)
    if sanitized_conf != conf_out:
        conf_out = sanitized_conf
    arg_list.append("--generated-conf-dir")
    arg_list.append(conf_out)


# \x1f as path raises exception, only on Windows.
################################################################################
def test_getPathException() -> None:
    """Pass an invalid path to buildnis, should raise an exception."""
    arg_list = ["-q", "--generated-conf-dir", "\x1f"]
    if platform.system() == "Windows":
        with pytest.raises(expected_exception=(OSError)):
            runBuildnis(arg_list)


# "\x1f\000" Null byte raises ValueError exception.
################################################################################
def test_getNullException() -> None:
    """Pass an invalid path to buildnis, should raise an exception."""
    arg_list = ["-q", "--generated-conf-dir", "\x1f\000"]

    with pytest.raises(expected_exception=ValueError):
        runBuildnis(arg_list)


################################################################################
def test_runClean() -> None:
    """Run `buildnis` with the argument `--clean` to remove generated build data"""
    try:
        runBuildnis(["--clean"])
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec


################################################################################
@settings(max_examples=10, deadline=None)
@given(arg=st.sampled_from(elements=["-q", "", "-v", "-vv"]))
def test_runSecondTime(arg: str) -> None:
    """Run Buildnis for the second time.

    Args:
        arg (str): The verbosity argument.
    """
    try:
        arg_list = []
        if arg != "":
            arg_list.append(arg)

        runBuildnis(arg_list)
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec


################################################################################
def test_runDistClean() -> None:
    """Run `buildnis` with the argument `--distclean` to remove  all generated data"""
    try:
        runBuildnis(["--distclean"])
    except SystemExit as excp:
        assert str(excp) == "0"  # nosec
