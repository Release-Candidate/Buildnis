# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     Config.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import logging
from modules.helpers.json import getJSONDict, readJSON, writeJSON
from modules.helpers import LOGGER_NAME
import os
import pprint
from modules.config import BUILD_FILE_NAME, FilePath, MODULE_FILE_NAME, PROJECT_FILE_NAME, CFG_VERSION

# TODO add protocols for config classes

class Config:
    """Loads all JSON configurations.

    Parses the project's JSON configuration, all module JSON configurations and
    all build tool JSON configurations.

    Attributes:

    config_path (FilePath): the path to the project's main JSON configuration.    
    project_cfg_dir (FilePath): The directory part of `config_path`
    project_cfg (obj): the project's JSON configuration stored in a Python class.
    module_cfgs (Dict[FilePath, Any]) the module JSON configurations (mentioned in project_cfg)
    build_cfgs (Dict[FilePath, Any]) the build JSON configurations (mentioned in the module JSONs)
    _logger (logging.Logger): the logger to use

    Methods:

    parseModuleCfgs: Parses the module JSON configurations setup in the project
                    JSON
    parseBuildCfgs: Parses the build JSON configurations setup in the module
                    JSONs
    setHostConfigPath: Sets the path to the generated host config file
    setBuildToolCfgPath: Sets the path to the generated build tool config file
    setProjDepCfgPath: Sets the path to the generated project dependency config file
    getProjCfgDict: Get the project configuration as a JSON sequenceable dict
    """
    ###########################################################################
    def __init__(self, project_config: FilePath) -> None:
        """Constructor of class Config.

        Parses the project's JSON configuration and stores it to project_cfg.

        Parameters:
            project_config: the path to the project's JSON configuration file.
        """
        self._logger = logging.getLogger(LOGGER_NAME)
        self.config_path = project_config

        self.project_cfg = readJSON(
            json_path=self.config_path, file_text="project", conf_file_name=PROJECT_FILE_NAME)

        self.project_cfg.project_dependency_config = os.path.abspath("/".join([
            os.path.dirname(self.config_path), os.path.basename(self.project_cfg.project_dependency_config)]))

        self.project_cfg_dir = os.path.abspath(os.path.dirname(self.config_path))

        self.module_cfgs = dict()

        self.build_cfgs = dict()

        self.parseModuleCfgs()

        self.parseBuildCfgs()

    ###########################################################################
    def parseModuleCfgs(self) -> None:
        """Parses the module JSON configurations.

        Parses and stores all module JSON configurations configured in the
        project's setup stored in self.project_cfg. Stores the configurations
        in module_cfgs.
        """
        for target in self.project_cfg.target:
            
            module_path = os.path.abspath(os.path.join(
                self.project_cfg_dir, target.module_file))

            module_cfg = readJSON(
                json_path=module_path, file_text="module", conf_file_name=MODULE_FILE_NAME)

            target.module_file = module_path

            module_cfg.module_path = os.path.normpath(os.path.dirname(
                module_path))

            self.module_cfgs[module_path] = module_cfg       

    ###########################################################################
    def parseBuildCfgs(self) -> None:
        """Parses the build JSON configurations.

        Parses and stores all module JSON configurations configured in the
        modules setups stored in self.module_cfgs. Stores the configurations
        in build_cfgs.
        """
        for mdl_key in self.module_cfgs:
            module_cfg = self.module_cfgs[mdl_key]

            for module_build_cfg in module_cfg.supported_builds:                                
                build_cfg_path = os.path.abspath(os.path.join(module_cfg.module_path,
                            module_build_cfg.build_config_file))

                build_cfg = readJSON(
                    json_path=build_cfg_path, file_text="build", conf_file_name=BUILD_FILE_NAME)

                build_cfg.build_cfg_path = os.path.normpath(os.path.dirname(
                    build_cfg_path))

                module_build_cfg.build_config_file = build_cfg_path          

                self.build_cfgs[build_cfg_path] = build_cfg

    ###########################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the project's config to a JSON file

        Args:
            json_path (str):  the path to write the json file to
        """       
        writeJSON(self.returnJSONComp(), json_path=json_path, 
                file_text="project", conf_file_name=PROJECT_FILE_NAME)
    
    ###########################################################################
    def returnJSONComp(self) -> dict:
        """Returns a JSON compatible version of `self.project_cfg`.
       
        Returns:
            dict: a JSON compatible version of `self.project_cfg`
        """
        ret_val = getJSONDict(self.project_cfg)          

        return ret_val

    ###########################################################################
    def setHostConfigPath(self, path: FilePath) -> None:
        """Sets the path to the generated host config JSON file.

        Args:
            path (FilePath): the path to the host config file
        """
        self.project_cfg.host_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setBuildToolCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated build tools config JSON file.

        Args:
            path (FilePath): the path to the build tools config file
        """
        self.project_cfg.build_tools_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setProjDepCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated project dependency config JSON file.

        Args:
            path (FilePath): the path to the project dependency config file.
        """
        self.project_cfg.project_dependency_config = os.path.abspath(path)

    ###########################################################################
    def __repr__(self) -> str:
        """Returns a string representing the object.

        Returns:
            str: A strings representation of the objects data
        """
        return pprint.pformat(vars(self))


                



