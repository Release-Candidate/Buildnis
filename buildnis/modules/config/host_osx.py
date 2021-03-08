# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host_osx.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

from buildnis.modules.config import CmdOutput
from buildnis.modules.helpers.execute import ExeArgs, runCommand


################################################################################
def getOSName() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sw_vers", ["-productVersion"]))


################################################################################
def getCPUNameOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "machdep.cpu.brand_string"]))


################################################################################
def getNumCoresOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.physicalcpu"]))


################################################################################
def getNumLogCoresOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.logicalcpu"]))


################################################################################
def getL2CacheOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.l2cachesize"]))


################################################################################
def getL3CacheOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.l3cachesize"]))


################################################################################
def getRAMSizeOSX() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("sysctl", ["-n", "hw.memsize"]))
