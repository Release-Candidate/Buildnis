# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     Config.py
# Date:     13.Feb.2021
###############################################################################

import json, io, sys, pathlib, os
from modules.config import BUILD_FILE_NAME, MODULE_FILE_NAME, PROJECT_FILE_NAME, VERSION
from types import SimpleNamespace


class Config:
    '''
    Loads all JSON configurations.

    Parses the project's JSON configuration, all module JSON configurations and
    all build tool JSON configurations.

    Attributes:

    config_path the path to the project'S main JSON configuration.
    project_cfg_dir The directory part of `config_path`
    project_cfg the project's JSON configuration stored in a Python class.
    module_cfgs the module JSON configurations (mentioned in project_cfg)
    build_cfgs the build JSON configurations (mentioned in the module JSONs)

    Methods:

    parseModuleCfgs Parses the module JSON configurations setup in the project
                    JSON
    parseBuildCfgs Parses the build JSON configurations setup in the module
                    JSONs
    '''
    ###########################################################################
    def __init__(self, project_config):
        '''
        Constructor of class Config.

        Parses the project's JSON configuration and stores it to project_cfg.

        Parameters:
        project_config the path to the project's JSON configuration file.
        '''
        self.config_path = project_config

        try:
            with io.open(self.config_path, mode= "r", encoding="utf-8") as file:
                self.project_cfg = json.load(file, object_hook=lambda dict: SimpleNamespace(**dict))

        except Exception as exp:
            print("ERROR: error \"{error}\" parsing file \"{path}\"".format(error=exp, path=self.config_path))
            sys.exit(4)

        if self.project_cfg.file_name != PROJECT_FILE_NAME:
            print("ERROR: project file \"{path}\" is not a valid project file!".format(path=self.config_path))
            print("ERROR: the value of 'file_name' should be \"{should}\" but is \"{but_is}\""
                    .format(should=PROJECT_FILE_NAME,but_is=self.project_cfg.file_name))
            sys.exit(5)

        file_major, file_minor = self.project_cfg.file_version.split(sep=".")
        if file_major < VERSION.major or file_minor < VERSION.minor:
            print("ERROR: project file \"{path}\" is not a valid project file!".format(
                path=self.config_path))
            print("ERROR: project file version (the value of 'file_version') is too old. is \"{old}\" should be \"{new}\""
                  .format(old=self.project_cfg.file_version, new=".".join(VERSION)))
            sys.exit(5)

        self.project_cfg_dir = os.path.normpath(os.path.dirname(self.config_path))

        self.module_cfgs = dict()

        self.build_cfgs = dict()

        self.parseModuleCfgs()

        self.parseBuildCfgs()

    ###########################################################################
    def parseModuleCfgs(self) -> None:
        '''
        Parses the module JSON configurations.

        Parses and stores all module JSON configurations configured in the
        project's setup stored in self.project_cfg. Stores the configurations
        in module_cfgs.
        '''
        for target in self.project_cfg.target:
            
            module_path = os.path.normpath(os.path.join(
                self.project_cfg_dir, target.module_file))

            if not pathlib.Path(module_path).is_file():
                print("ERROR: module configuration file \"{config}\" not found or is not a file!".format(
                    config=module_path))
                sys.exit(2)
            try:
                with io.open(module_path, mode= "r", encoding="utf-8") as file:
                    module_cfg = json.load(file, object_hook=lambda dict: SimpleNamespace(**dict))

            except Exception as exp:
                print("ERROR: error \"{error}\" parsing file \"{path}\"".format(error=exp, path=module_path))
                sys.exit(4)

            if module_cfg.file_name != MODULE_FILE_NAME:
                print("ERROR: module file \"{path}\" is not a valid module file!".format(path=module_path))
                print("ERROR: the value of 'file_name' should be \"{should}\" but is \"{but_is}\""
                     .format(should=MODULE_FILE_NAME,but_is=module_cfg.file_name))
                sys.exit(5)

            file_major, file_minor = module_cfg.file_version.split(sep=".")
            
            if file_major < VERSION.major or file_minor < VERSION.minor:
                print("ERROR: module file \"{path}\" is not a valid module file!".format(
                    path=module_path))
                print("ERROR: module file version (the value of 'file_version') is too old. is \"{old}\" should be \"{new}\""
                  .format(old=module_cfg.file_version, new=".".join(VERSION)))
                sys.exit(5)

            target.module_file = module_path

            module_cfg.module_path = os.path.normpath(os.path.dirname(
                module_path))

            self.module_cfgs[module_path] = module_cfg       

    ###########################################################################
    def parseBuildCfgs(self) -> None:
        '''
        Parses the build JSON configurations.

        Parses and stores all module JSON configurations configured in the
        modules setups stored in self.module_cfgs. Stores the configurations
        in build_cfgs.
        '''
        for mdl_key in self.module_cfgs:
            module_cfg = self.module_cfgs[mdl_key]

            for module_build_cfg in module_cfg.supported_builds:                                
                build_cfg_path = os.path.normpath(os.path.join(module_cfg.module_path,
                            module_build_cfg.build_config_file))

                if build_cfg_path in self.build_cfgs:
                    continue
               
                if not pathlib.Path(build_cfg_path).is_file():
                    print("ERROR: build configuration file \"{config}\" not found or is not a file!".format(
                        config=build_cfg_path))
                    sys.exit(2)
                try:
                    with io.open(build_cfg_path, mode="r", encoding="utf-8") as file:
                        build_cfg = json.load(
                            file, object_hook=lambda dict: SimpleNamespace(**dict))

                except Exception as exp:
                    print("ERROR: error \"{error}\" parsing file \"{path}\"".format(
                        error=exp, path=build_cfg_path))
                    sys.exit(4)

                if build_cfg.file_name != BUILD_FILE_NAME:
                    print("ERROR: build config file \"{path}\" is not a valid build config file!".format(
                        path=build_cfg_path))
                    print("ERROR: the value of 'file_name' should be \"{should}\" but is \"{but_is}\""
                          .format(should=BUILD_FILE_NAME, but_is=build_cfg.file_name))
                    sys.exit(5)

                file_major, file_minor = build_cfg.file_version.split(sep=".")

                if file_major < VERSION.major or file_minor < VERSION.minor:
                    print("ERROR: build config file \"{path}\" is not a valid build config file!".format(
                        path=build_cfg_path))
                    print("ERROR: build config file version (the value of 'file_version') is too old. is \"{old}\" should be \"{new}\""
                          .format(old=build_cfg.file_version, new=".".join(VERSION)))
                    sys.exit(5)            

                build_cfg.build_cfg_path = os.path.normpath(os.path.dirname(
                    build_cfg_path))

                module_build_cfg.build_config_file = build_cfg_path          

                self.build_cfgs[build_cfg_path] = build_cfg

        print(self.project_cfg.__dict__)

        print("=======================================================")

        for module_key in self.module_cfgs:
            print(module_key, self.module_cfgs[module_key].__dict__)
            print("")

        print("=======================================================")
        
        for build_key in self.build_cfgs:
            print(build_key, self.build_cfgs[build_key].__dict__)
            print("")


                



