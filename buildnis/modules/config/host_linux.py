# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host_linux.py
# Date:     08.Mar.2021
###############################################################################

from __future__ import annotations

from buildnis.modules.config import CmdOutput
from buildnis.modules.helpers.execute import ExeArgs, runCommand


################################################################################
def getOSMajVers() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            [
                "-c",
                "grep NAME /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
            ],
        )
    )


################################################################################
def getOSVer() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            [
                "-c",
                "grep VERSION /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
            ],
        )
    )


################################################################################
def getCPUNameLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep 'model name' /proc/cpuinfo |head -1|cut -d':' -f2-"],
        )
    )


################################################################################
def getNumCoresLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep 'cpu cores' /proc/cpuinfo |uniq|cut -d':' -f2"],
        )
    )


################################################################################
def getNumLogCoresLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "grep siblings /proc/cpuinfo |uniq |cut -d':' -f2"],
        )
    )


################################################################################
def getL2CacheLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "getconf -a|grep LEVEL2_CACHE_SIZE|awk '{print $2}'"],
        )
    )


################################################################################
def getL3CacheLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs(
            "bash",
            ["-c", "getconf -a|grep LEVEL3_CACHE_SIZE|awk '{print $2}'"],
        )
    )


################################################################################
def getRAMSizeLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs("bash", ["-c", "free -b|grep 'Mem:'|awk '{print $2}'"])
    )


################################################################################
def getGPUNamesLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(exe_args=ExeArgs("bash", ["-c", "lspci|grep VGA|cut -f3 -d':'"]))


################################################################################
def getGPUNamesSbinLinux() -> CmdOutput:
    """[summary]

    Returns:
        CmdOutput: [description]
    """
    return runCommand(
        exe_args=ExeArgs("bash", ["-c", "/sbin/lspci|grep VGA|cut -f3 -d':'"])
    )
