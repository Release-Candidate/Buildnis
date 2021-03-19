# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     test_files.py
# Date:     18.Mar.2021
###############################################################################

from __future__ import annotations

import ctypes
import os
import pathlib
import platform
import tempfile
from typing import Callable

import pytest

import tests
from buildnis.modules.config import FilePath
from buildnis.modules.helpers import files


################################################################################
@pytest.mark.fast
@pytest.mark.parametrize(
    "func",
    [
        pytest.param(files.checkIfExists, id="checkIfExists"),
        pytest.param(files.checkIfIsFile, id="checkIfIsFile"),
        pytest.param(files.checkIfIsDir, id="checkIfIsDir"),
        pytest.param(files.checkIfIsLink, id="checkIfIsLink"),
        pytest.param(files.makeDirIfNotExists, id="makeDirIfNotExists"),
        pytest.param(files.hashFile, id="hashFile"),
        pytest.param(files.returnExistingFile, id="returnExistingFile"),
    ],
)
def test_checkIfRaisesExcp(func: Callable[[FilePath], bool]) -> None:
    """Test functions with an invalid path."""
    file_path = "\x1f"
    if platform.system() == "Windows":
        with pytest.raises(files.FileCompareException):
            func(file_path)


################################################################################
@pytest.mark.fast
@pytest.mark.parametrize(
    "func",
    [
        pytest.param(files.deleteDirs, id="deleteDirs"),
        pytest.param(files.deleteFiles, id="deleteFiles"),
    ],
)
def test_checkIfRaisesExcpLogger(test_logger, func: Callable[[FilePath], bool]) -> None:
    """Test functions that take a logger as first argument with an invalid path."""
    file_path = "\x1f"
    if platform.system() == "Windows":
        with pytest.raises(files.FileCompareException):
            func(test_logger, file_path)


################################################################################
@pytest.mark.fast
@pytest.mark.parametrize(
    "func",
    [
        pytest.param(files.makeDirIfNotExists, id="makeDirIfNotExists"),
        pytest.param(files.hashFile, id="hashFile"),
        pytest.param(files.returnExistingFile, id="returnExistingFile"),
    ],
)
def test_checkIfIs(func: Callable[[FilePath], bool]) -> None:
    """Test functions with an invalid path."""
    file_path = "\x1f"
    if platform.system() == "Windows":
        with pytest.raises(files.FileCompareException):
            func(file_path)


################################################################################
@pytest.mark.fast
def test_checkIfExists() -> None:
    """Check if the given path exists, is a file or directory."""
    file_path1 = tests.test_project_path
    file_path2 = "/".join([tests.test_project_path, "project_config.json"])
    file_path3 = "/".join([tests.test_project_path, "this_does_not_exist"])
    files_to_test = {
        file_path1: True,
        file_path2: True,
        file_path3: False,
    }
    for file_path in files_to_test:
        assert files.checkIfExists(file_path) == files_to_test[file_path]  # nosec


################################################################################
@pytest.mark.fast
def test_checkIfIsFile() -> None:
    """Check if the path points to a file"""
    file_path1 = "/".join([tests.test_project_path, "project_config.json"])
    file_path2 = "/".join([tests.test_project_path, "this_does_not_exist"])
    files_to_test = {
        file_path1: True,
        file_path2: False,
    }
    for file_path in files_to_test:
        assert files.checkIfIsFile(file_path) == files_to_test[file_path]  # nosec


################################################################################
@pytest.mark.fast
def test_checkIfIsDir() -> None:
    """Check if the path points to a directory."""
    file_path1 = tests.test_project_path
    file_path2 = "/".join([tests.test_project_path, "project_config.json"])  # file
    file_path3 = "/".join([tests.test_project_path, "this_does_not_exist"])
    files_to_test = {
        file_path1: True,
        file_path2: False,
        file_path3: False,
    }
    for file_path in files_to_test:
        assert files.checkIfIsDir(file_path) == files_to_test[file_path]  # nosec


################################################################################
@pytest.mark.fast
def test_checkIfIsLink() -> None:
    """Check if the path points to a link."""
    with tempfile.TemporaryDirectory(dir=tests.test_project_path) as temp_dir:
        temp_dir_name = temp_dir
        file_path1 = os.path.abspath("/".join([temp_dir_name, "to_test"]))
        file_path2 = tests.test_project_path
        link_target = os.path.abspath(
            "/".join([tests.test_project_path, "project_config.json"])
        )

        # on Windows you need administrator privileges to link
        if (
            platform.system() == "Windows"
            and ctypes.windll.shell32.IsUserAnAdmin() == 0
        ):
            with pytest.raises(expected_exception=OSError) as excp:
                os.symlink(src=link_target, dst=file_path1)
            assert excp  # nosec

        else:
            os.symlink(src=link_target, dst=file_path1)
            files_to_test = {
                file_path1: True,
                file_path2: False,
            }
            for file_path in files_to_test:
                assert (  # nosec
                    files.checkIfIsLink(file_path) == files_to_test[file_path]
                )


################################################################################
@pytest.mark.fast
def test_makeDIrIfNotExist() -> None:
    """Test the function `makeDirIfNotExists`."""
    file_path1 = tests.test_project_path
    file_path2 = "/".join([tests.test_project_path, "project_config.json"])  # file
    file_path3 = "/".join([tests.test_project_path, "this_does_not_exist"])

    files.makeDirIfNotExists(directory=file_path1)
    assert pathlib.Path(file_path1).is_dir()  # nosec

    with pytest.raises(expected_exception=files.FileCompareException) as excp:
        files.makeDirIfNotExists(directory=file_path2)
    assert excp  # nosec

    assert not pathlib.Path(file_path3).exists()  # nosec
    files.makeDirIfNotExists(directory=file_path3)
    assert pathlib.Path(file_path3).is_dir()  # nosec
    pathlib.Path(file_path3).rmdir()


################################################################################
@pytest.mark.fast
def test_hashFile() -> None:
    """Test the BLAKE2 checksum function."""
    file_path1 = tests.test_project_path
    file_path2 = "/".join([tests.test_project_path, "project_config.json"])  # file
    file_path3 = "/".join([tests.test_project_path, "this_does_not_exist"])

    with pytest.raises(expected_exception=files.FileCompareException) as excp:
        files.hashFile(file=file_path1)
    assert excp  # nosec

    hex_hash = files.hashFile(file=file_path2)
    assert hex_hash != ""  # nosec

    with pytest.raises(expected_exception=files.FileCompareException) as excp:
        files.hashFile(file=file_path3)
    assert excp  # nosec


################################################################################
@pytest.mark.fast
def test_returnExistingFile() -> None:
    """Test the function `returnExistingFile`."""
    file_path1 = tests.test_project_path
    file_path2 = "/".join([tests.test_project_path, "project_config.json"])  # file
    file_path3 = "/".join([tests.test_project_path, "this_does_not_exist"])

    assert (  # nosec
        files.returnExistingFile(file_list=[file_path1, file_path3]) == file_path1
    )

    assert (  # nosec
        files.returnExistingFile(file_list=[file_path2, file_path3]) == file_path2
    )

    assert (  # nosec
        files.returnExistingFile(file_list=[file_path1, file_path2, file_path3])
        == file_path1
    )


################################################################################
@pytest.mark.fast
def test_deleteDirs(test_logger) -> None:
    """Test the function `deleteDirs`."""
    dirs_to_delete = []
    for i in range(1, 10):
        i
        dirs_to_delete.append(tempfile.mkdtemp(dir=tests.test_project_path))
    files.deleteDirs(test_logger, list_of_dirs=dirs_to_delete)
    for del_dir in dirs_to_delete:
        assert not pathlib.Path(del_dir).exists()  # nosec


###############################################################################
@pytest.mark.fast
def test_deleteFiles(test_logger) -> None:
    """Test the function `deleteFiles`."""
    files_to_delete = []
    for i in range(1, 10):
        i
        file_hdl, file_name = tempfile.mkstemp(dir=tests.test_project_path)
        os.close(file_hdl)
        files_to_delete.append(file_name)
    files.deleteFiles(test_logger, list_of_files=files_to_delete)
    for del_dir in files_to_delete:
        assert not pathlib.Path(del_dir).exists()  # nosec
