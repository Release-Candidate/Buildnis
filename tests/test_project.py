# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     test_project.py
# Date:     16.Mar.2021
###############################################################################

from __future__ import annotations

import pathlib
import platform
import runpy
import sys
from typing import List

import pathvalidate
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

import tests


################################################################################
def setup_module(test_project) -> None:
    """Set the path to write the generated documentation to."""


################################################################################
def teardown_module(test_project) -> None:
    """Delete the whole directory including the generated files."""
    if pathlib.Path(tests.config_dir_abs).exists():

        for directory in pathlib.Path(tests.config_dir_abs).glob("*"):
            for config in pathlib.Path(directory).glob("*"):
                pathlib.Path(config).unlink()
            pathlib.Path(directory).rmdir()

        pathlib.Path(tests.config_dir_abs).rmdir()


################################################################################
def runBuildnis(cmd_line_args: List[str]) -> None:
    """Run the program with the given arguments.

    Returns the output of the command in the tuple `stdout, stderr`. The first element
    of the tuple holds the process' output on `stdout`, the second the output on
    `stderr`.

    Args:
        cmd_line_args (List[str]): The arguments to pass to `buildnis`.
    """
    sys_argv_list = [""]
    sys_argv_list.extend(cmd_line_args)
    sys_argv_list.append("./test_project/project_config.json")
    sys.argv = sys_argv_list

    runpy.run_module("buildnis", run_name="__main__")


################################################################################
@pytest.mark.fast
@pytest.mark.run_program
def test_runVersion() -> None:
    """Run `buildnis` with the argument `--version` to show the version information."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        runBuildnis(["--version"])
    assert excp.value.args[0] == 0  # nosec


################################################################################
@pytest.mark.fast
@pytest.mark.run_program
def test_runHelp() -> None:
    """Run `buildnis` with the argument `--help` to show the usage information."""
    with pytest.raises(expected_exception=SystemExit) as excp:
        runBuildnis(["--help"])
    assert excp.value.args[0] == 0  # nosec


################################################################################
@pytest.mark.slow
@pytest.mark.run_program
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
    with pytest.raises(expected_exception=SystemExit) as excp:
        arg_list = []
        if arg != "":
            arg_list.append(arg)
        if conf_out != "":
            sanitizePath(conf_out, arg_list)

        runBuildnis(arg_list)
    assert excp.value.args[0] == 0  # nosec


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
    arg_list.append("/".join([tests.config_dir, conf_out]))


# \x1f as path raises exception, only on Windows.
################################################################################
@pytest.mark.fast
@pytest.mark.run_program
def test_getPathException() -> None:
    """Pass an invalid path to buildnis, should raise an exception."""
    arg_list = ["-q", "--generated-conf-dir", "\x1f"]
    if platform.system() == "Windows":
        with pytest.raises(expected_exception=(OSError, SystemExit)):
            runBuildnis(arg_list)


# "\x1f\000" Null byte raises ValueError exception.
################################################################################
@pytest.mark.fast
@pytest.mark.run_program
def test_getNullException() -> None:
    """Pass an invalid path to buildnis, should raise an exception."""
    arg_list = ["-q", "--generated-conf-dir", "\x1f\000"]

    with pytest.raises(expected_exception=(ValueError, SystemExit)):
        runBuildnis(arg_list)


################################################################################
@pytest.mark.run_program
def test_runClean() -> None:
    """Run `buildnis` with the argument `--clean` to remove generated build data"""
    with pytest.raises(expected_exception=SystemExit) as excp:
        runBuildnis(["--clean"])
    assert excp.value.args[0] == 0  # nosec


################################################################################
@pytest.mark.slow
@pytest.mark.run_program
@settings(max_examples=10, deadline=None)
@given(arg=st.sampled_from(elements=["-q", "", "-v", "-vv"]))
def test_runSecondTime(arg: str) -> None:
    """Run Buildnis for the second time.

    Args:
        arg (str): The verbosity argument.
    """
    with pytest.raises(expected_exception=SystemExit) as excp:
        arg_list = []
        if arg != "":
            arg_list.append(arg)

        runBuildnis(arg_list)

    assert excp.value.args[0] == 0  # nosec


################################################################################
@pytest.mark.run_program
def test_runDistClean() -> None:
    """Run `buildnis` with the argument `--distclean` to remove  all generated data"""
    with pytest.raises(expected_exception=SystemExit) as excp:
        runBuildnis(["--distclean"])

    assert excp.value.args[0] == 0  # nosec
