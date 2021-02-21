# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     check.py
# Date:     16.Feb.2021
###############################################################################

from __future__ import annotations
import logging
from modules.helpers.execute import doesExecutableWork, runCommand
from modules.helpers.json import writeJSON
from modules.helpers import LOGGER_NAME

import os
import sys
import json
import pathlib
import datetime
from types import SimpleNamespace
from typing import Any

from modules import EXT_ERR_DIR
from modules.config import Arch, BUILD_TOOL_CONFIG_NAME, CFG_VERSION, CONFIGURE_SCRIPTS_PATH, FilePath, OSName

class WriteCfg:
    """Helper class to encode Check.build_tools_cfgs to JSON.
    """

    ############################################################################
    def __init__(self, cfg_list: list) -> None: 
        """Converts the list of classes to a list of dictionaries suited to be 
        dumped by the JSON writer `json.dump`

        Args:           
            cfg_list (list): the list of generated build tool configs
        """
        
        self.file_name = BUILD_TOOL_CONFIG_NAME
        self.file_version = ".".join(CFG_VERSION)
        self.build_tool_cfgs = []
        self.generated_at = datetime.datetime.now(
            tz=None).isoformat(sep=" ", timespec="seconds")

        for cfg in cfg_list:            
            temp_dict = dict()
            try:
                temp_dict["name"] = cfg.name
            except AttributeError:
                temp_dict["name"] = ""
            try:
                temp_dict["name_long"] = cfg.name_long
            except AttributeError:
                temp_dict["name_long"] = ""
            try:
                temp_dict["version"] = cfg.version
            except AttributeError:
                temp_dict["version"] = ""
            try:
                temp_dict["build_tool_exe"] = cfg.build_tool_exe
            except AttributeError:
                temp_dict["build_tool_exe"] = ""
            try:
                temp_dict["install_path"] = cfg.install_path
            except AttributeError:
                temp_dict["install_path"] = ""
            try:
                temp_dict["env_script"] = cfg.env_script
            except AttributeError:
                temp_dict["env_script"] = ""
            try:
                temp_dict["env_script_arg"] = cfg.env_script_arg
            except AttributeError:
                temp_dict["env_script_arg"] = ""
            try:
                temp_dict["version_regex"] = cfg.version_regex
            except AttributeError:
                temp_dict["version_regex"] = ""
            try:
                temp_dict["version_arg"] = cfg.version_arg
            except AttributeError:
                temp_dict["version_arg"] = ""
            try:
                temp_dict["is_checked"] = cfg.is_checked
            except AttributeError:
                temp_dict["is_checked"] = False
            
            self.build_tool_cfgs.append(temp_dict) 

# TODO add protocol for the config class

class Check:
    """Checks if all build tools are present.
    
    Runs all build tool script_paths in `configure_script_paths` in the subdirectory 
    with the name of the OS passed to the constructor.

    Each build tool configuration (item of build_tool_cfgs) has the following 
    attributes:

    * `name`                The name of the build tool
    * `name_long`           The full name of the build tool
    * `version`             The version of the build tool, gathered from its output
    * `version_arg`         The argument to call the build tool with to get the version 
    * `version_regex`       The regex to parse the output of `version_arg` to get `version`
    * `build_tool_exe`      The executable's file name
    * `install_path`        The path to the executable
    * `env_script`          The environment script to call before using the executable
    * `env_script_arg`      The argument to call the environment script with
    * `is_checked`          Has the executable been run and the version output been parsed?

    Attributes:
        os_name (OSName): the OS we are building for
        arch (Arch): the CPU architecture we are building for
        build_tool_cfgs (list): the list of build tool configurations returned from 
                        the script_paths in `configure_script_paths/OS`
        _logger (logging.Logger): the logger to use

    Methods:
        writeJSON: writes the gathered build tool configurations to the given 
                    JSON config file.
        isBuildToolCfgOK: checks if the build tool config has the minimum 
                            needed attributes
        checkVersions: runs all build tools with the version argument, to check
                        if the executable works
    """
    ###########################################################################
    def __init__(self, os_name: OSName, arch: Arch) -> None:
        """Constructor of Check, runs all build tool script_paths in 
        `configure_script_paths`.

        All build tool script_paths in the `os` subdirectory of `configure_script_paths` 
        are run, the CPU architecture `arch` is passed as an argument to each
        script_path.

        Args:
            os_name (OSName): the OS we are building for
            arch (Arch): the CPU architecture we are building for
        """
        self.os = os_name
        self.arch = arch

        self._logger = logging.getLogger(LOGGER_NAME)

        working_dir = pathlib.Path(os.path.normpath(
            "/".join([CONFIGURE_SCRIPTS_PATH, os_name])))        
        if not working_dir.is_dir(): 
            self._logger.critical(
                "error: \"\{path}\" does not exist or is not a directory!".format(path=working_dir))
            sys.exit(EXT_ERR_DIR)
        
        self.build_tool_cfgs = []
        for script_path in working_dir.glob("*"): 
            try:
                if script_path.is_file():
            
                    self._logger.warning(
                        "Calling build tool config script \"{path}\"".format(path=script_path))
                    try:                      
                        script_out = runCommand(
                            exe=script_path, args=[self.arch])

                        build_tool_cfg = json.loads(
                            script_out.std_out, object_hook=lambda dict: SimpleNamespace(**dict))

                    except Exception as excp:
                        self._logger.error("error \"{error}\" running build tool script \"{path}\""
                                           .format(error=excp, path=script_path))

                    for item in build_tool_cfg.build_tools:
                        if self.isBuildToolCfgOK(item):
                            self.build_tool_cfgs.append(item)
                        else:
                            self._logger.error("build tool config \"{cfg}\" doesn't have all needed attributes!".format(
                                cfg=script_path))
            except Exception as excp:
                self._logger.error("build tool filename \"{cfg}\" not valid".format(
                    cfg=script_path))
        
        self.checkVersions()

    ############################################################################
    def isBuildToolCfgOK(self, cfg: Any) -> bool:
        """Checks if the given object has all the needed attributes of a build 
        tool configuration.

        Args:
            cfg (obj): the object to check

        Returns:
            bool: True, if `cfg` has all needed attributes
                  False else
        """
        try:
            cfg.name
        except AttributeError:
            print("ERROR: build config has no attribute \"name\"")
            return False
        try:
            cfg.name_long
        except AttributeError:
            cfg.name_long = ""
        try:
            cfg.version
        except AttributeError:
            cfg.version = ""
        try:
            cfg.build_tool_exe
        except AttributeError:
            self._logger.error(
                "ERROR: build config has no attribute \"build_tool_exe\"")
            return False
        try:
            cfg.install_path
        except AttributeError:
            cfg.install_path = ""
        try:
            cfg.env_script
        except AttributeError:
            cfg.env_script = ""
        try:
            cfg.env_script_arg
        except AttributeError:
            cfg.env_script_arg = ""
        try:
            cfg.version_regex
        except AttributeError:
            self._logger.error(
                "ERROR: build config has no attribute \"version_regex\"")
            return False
        try:
            cfg.version_arg
        except AttributeError:
            cfg.version_arg = ""

        return True
       
            

    ############################################################################
    def checkVersions(self) -> None:
        """Runs all configured build tools with the 'show version' argument.

        To check, if the configured build tools exist and are working, try to 
        execute each with the argument to get the version string of the build 
        tool.
        """ 
        for tool in self.build_tool_cfgs:
            if tool.build_tool_exe == "":
                self._logger.error("build tool \"{name}\" has no executable configured!".format(
                    name=tool.name))       
                continue

            exe_path = tool.build_tool_exe

            # has environment script to call
            if tool.env_script != "":
                self._logger.info("\"{name}\": calling environment script \"{script}\".".format(
                    name=tool.name, script=tool.env_script))            

            # has full path (so maybe not in PATH)
            elif tool.install_path != "":
                exe_path = os.path.normpath(
                    "/".join([tool.install_path, tool.build_tool_exe]))
                self._logger.info("\"{name}\": using path \"{path}\".".format(
                    name=tool.name, path=exe_path))
            
            # no full path given, so it hopefully is in PATH
            else:
                self._logger.info("\"{name}\": checking if executable \"{exe}\" is in PATH.".format(
                    name=tool.name, exe=tool.build_tool_exe))

            try:               
                tool.version = doesExecutableWork(exe=exe_path, check_regex=tool.version_regex, 
                                                regex_group=1, args=[tool.version_arg],
                                                env_script=tool.env_script, env_script_args=[tool.env_script_arg])
                if tool.version != "":
                    tool.is_checked = True

            except Exception as excp:
                self._logger.error("error \"{error}\" parsing version of \"{exe} {opt}\" using version regex \"{regex}\"".format(
                    error= excp, exe=exe_path, opt=tool.version_arg, regex=tool.version_regex))

    ############################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the gathered build tool configurations to a file.
        
        Args:
            json_path (FilePath): path to write the JSON build tools configuration to
        """       
        write_cfg = WriteCfg(self.build_tool_cfgs)
        writeJSON(write_cfg.__dict__, file_text="build tools", 
                json_path=json_path, conf_file_name=BUILD_TOOL_CONFIG_NAME)
        



    
