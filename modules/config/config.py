# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     Config.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import os

from modules.config.json_base_class import JSONBaseClass
from modules.helpers.json import readJSON
from modules.config import BUILD_FILE_NAME, FilePath, MODULE_FILE_NAME, PROJECT_FILE_NAME, config_values, project_dependency


class Config(JSONBaseClass):
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
        super().__init__(config_file_name=PROJECT_FILE_NAME, config_name="project")

        self.project_dep_cfg: project_dependency.ProjectDependency = None        
        self.config_path = project_config

        self.readJSON(json_path=self.config_path)

        # self.project_cfg = readJSON(
        #     json_path=self.config_path, file_text="project", conf_file_name=PROJECT_FILE_NAME)

        self.project_dependency_config = os.path.abspath("/".join([
            os.path.dirname(self.config_path), os.path.basename(self.project_dependency_config)]))

        self.project_cfg_dir = os.path.abspath(
            os.path.dirname(self.config_path))

        must_have_attrs = ["config_path", "email",
                           "web_url", "copyright_info", "company", "author", "version", "name"]
        for attr in must_have_attrs:
            if not hasattr(self, attr): 
                setattr(self, attr, "")
       
        config_values.PROJECT_CONFIG_DIR_PATH = self.project_cfg_dir
        config_values.PROJECT_NAME = self.name
        config_values.PROJECT_VERSION = self.version
        config_values.PROJECT_AUTHOR = self.author
        config_values.PROJECT_COMPANY = self.company
        config_values.PROJECT_COPYRIGHT_INFO = self.copyright_info
        config_values.PROJECT_WEB_URL = self.web_url
        config_values.PROJECT_EMAIL = self.email
        config_values.PROJECT_ROOT = os.path.abspath(
            os.path.dirname(self.config_path))

        self.module_cfgs = []

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
        tmp_module_paths = []
        for module in self.modules:

            module_path = os.path.abspath(os.path.join(
                self.project_cfg_dir, module))

            module_cfg = readJSON(
                json_path=module_path, file_text="module", conf_file_name=MODULE_FILE_NAME)

            tmp_module_paths.append(module_path)

            module_cfg.module_path = os.path.normpath(os.path.dirname(
                module_path))

            self.module_cfgs.append(module_cfg)

            self.modules = tmp_module_paths

    ###########################################################################
    def parseBuildCfgs(self) -> None:
        """Parses the build JSON configurations.

        Parses and stores all module JSON configurations configured in the
        modules setups stored in self.module_cfgs. Stores the configurations
        in build_cfgs.
        """
        for module_cfg in self.module_cfgs:           

            for module_build_cfg in module_cfg.supported_builds:
                build_cfg_path = os.path.abspath(os.path.join(module_cfg.module_path,
                                                              module_build_cfg.build_config_file))

                build_cfg = readJSON(
                    json_path=build_cfg_path, file_text="build", conf_file_name=BUILD_FILE_NAME)

                build_cfg.build_cfg_path = os.path.normpath(os.path.dirname(
                    build_cfg_path))

                module_build_cfg.build_config_file = build_cfg_path

                self.build_cfgs[build_cfg_path] = build_cfg

    ############################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the project's config to a JSON file

        Args:
            json_path (str):  the path to write the json file to
        """
        super().writeJSON(json_path=json_path, to_ignore=[
            "module_cfgs", "project_dep_cfg"])

    ###########################################################################
    def setHostConfigPath(self, path: FilePath) -> None:
        """Sets the path to the generated host config JSON file.

        Args:
            path (FilePath): the path to the host config file
        """
        self.host_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setBuildToolCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated build tools config JSON file.

        Args:
            path (FilePath): the path to the build tools config file
        """
        self.build_tools_cfg_file = os.path.abspath(path)

    ###########################################################################
    def setProjDepCfgPath(self, path: FilePath) -> None:
        """Sets the path to the generated project dependency config JSON file.

        Args:
            path (FilePath): the path to the project dependency config file.
        """
        self.project_dependency_config_file = os.path.abspath(path)

    ###########################################################################
    def expandAllPlaceholders(self) -> None:
        """Goes through all configurations and replaces placeholders in their
        elements. A Placeholder is a string like `${PLACEHOLDER}`, a dollar
        sign followed by a curly opening brace, the string to replace and the 
        closing curly brace.       
        """
        super().expandAllPlaceholders()
        # # for key in self.project_cfg.__dict__:
        # #     # print("Project {key}: {value}".format(key=key, value=self.project_cfg.__dict__[key]))
        # #     self.project_cfg.__dict__[key] = parseConfigElement(element=self.project_cfg.__dict__[key], parents=[self.project_cfg])
        # self.project_cfg = parseConfigElement(
        #     element=self, parents=[self])

        # for module in self.module_cfgs:
        #     # for key in self.module_cfgs[module].__dict__:
        #     #     # print("Module {key}: {value}".format(key=key,
        #     #     #                                      value=self.module_cfgs[module].__dict__[key]))
        #     #     self.module_cfgs[module].__dict__[key] = parseConfigElement(element=self.module_cfgs[module].__dict__[
        #     #         key], parents=[self.project_cfg])
        #     self.module_cfgs[module] = parseConfigElement(
        #         element=self.module_cfgs[module], parents=[self.project_cfg, self.module_cfgs[module]])

        # for build_cfg in self.build_cfgs:
        #     # for key in build_cfg.__dict__:
        #     #     print("Build CFG {key}: {value}".format(key=key,
        #     #                                             value=build_cfg[key]))
        #     #     self.build_cfgs[build_cfg].__dict__[key] = parseConfigElement(element=self.build_cfgs[build_cfg].__dict__[
        #     #                        key], parents=[self.project_cfg])
        #     self.build_cfgs[build_cfg] = parseConfigElement(
        #         element=self.build_cfgs[build_cfg], parents=[self.project_cfg, self.build_cfgs[build_cfg]])

        # # for key in self.project_dep_cfg.dependency_cfg.__dict__:
        # #     # print("Dep CFG {key}: {value}".format(key=key,
        # #     #                                       value=self.project_dep_cfg.dependency_cfg.__dict__[key]))
        # #     self.project_dep_cfg.dependency_cfg.__dict__[key] = parseConfigElement(
        # #         element=self.project_dep_cfg.dependency_cfg.__dict__[key], parents=[self.project_cfg])
        # self.project_dep_cfg.dependency_cfg = parseConfigElement(
        #     element=self.project_dep_cfg.dependency_cfg, parents=[self.project_cfg, self.project_dep_cfg.dependency_cfg])

    ###########################################################################
    def checkDependencies(self, force_check: bool = False) -> None:
        """Calls the `checkDependencies` method of the project dependency 
        configuration.

        Args:
            force_check (bool, optional): if this is `True`, check the 
                        dependency even if it has been checked before - if 
                        `is_checked` is `True`. Defaults to False.
        """
        if self.project_dep_cfg != None:
            self.project_dep_cfg.checkDependencies(force_check)

    # ###########################################################################
    # def __repr__(self) -> str:
    #     """Returns a string representing the object.

    #     Returns:
    #         str: A strings representation of the objects data
    #     """
    #     return pprint.pformat(getJSONDict(self.project_cfg), indent=4, sort_dicts=False)
