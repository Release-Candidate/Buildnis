# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     project_dependency.py
# Date:     19.Feb.2021
###############################################################################

from types import SimpleNamespace
from modules import EXT_ERR_LD_FILE, EXT_ERR_NOT_VLD, EXT_ERR_WR_FILE
import os
import io
import sys
import json
import pathlib
import datetime
from typing import Dict, List
from modules.config import CFG_VERSION, FilePath, PROJECT_DEP_FILE_NAME

###############################################################################
class ProjDepConfig:
    """A class to hold all values of a project dependency configuration in its
    attributes.

    Attributes:

        file_name (str): the JSON configuration file ID, should be `PROJECT_DEP_FILE_NAME`
        file_version (str): the version of the JSON configuration file.
        generated_at (str): the date and time this configuration has been checked
        dependencies (List[Dict]): the list of actual dependencies.

    Keys of dependency dictionary:

        name (str): the dependency's name
        website_url (str): website to get information about the dependency
        download_url (str): website to download the dependency
        download_dir (str): path to the directory to download the dependency to
        install_cmd (str): command line to call to install the dependency
        ok_if_exists (FilePath): if this file exists, the dependency has been 
                                 successfully installed
        ok_if_executable (FilePath): if this file is executable, the dependency 
                                     has been successfully installed 
        executable_argument (str): the argument to call `ok_if_executable` with
                                    to test it
        executable_check_regex (str): the regex to parse the output of 
                                      `ok_if_executable` with. If a match is 
                                      found,  the dependency has been 
                                      successfully installed 
        is_checked (bool): if this is true, the dependency has been successfully 
                            installed

    """
    ############################################################################
    def __init__(self, src: object) -> None:
        """Constructs a full project dependency configuration object from 
        the object `src`.

        Args:
            src (object): the object holding the project dependency
                        configuration values read from the JSON
        """
        try:
            self.file_name: str = src.file_name
        except AttributeError:
            self.file_name = PROJECT_DEP_FILE_NAME
        try:
            self.file_version: str = src.file_version
        except AttributeError:
            self.file_version: str = ".".join(CFG_VERSION)
        try:
            self.generated_at: str = src.generated_at
        except AttributeError:
            self.generated_at: str = ""
        try:
            tmp_list = src.dependencies
        except AttributeError:
            self.dependencies: List[object] = []
        
        if tmp_list == None:
            self.dependencies = []

        tmp_dep = []
        for dep in tmp_list:
            tmp_dep.append(self.depObjToDict(dep))
        
        self.dependencies = tmp_dep

    ############################################################################
    def depObjToDict(self, dependency: object) -> Dict[str, str]:
        """Creates a dictionary from the values of the given object `dependency`.

        Nonexistent values get initialized.

        Args:
            dependency (object): the object containing the parsed dependency

        Returns:
            Dict[str, str]: a dictionary of the values of the given object.
        """
        ret_val = dict()
        try:
            ret_val["name"] = dependency.name
        except AttributeError:
            ret_val["name"] = ""
        try:
            ret_val["website_url"] = dependency.website_url
        except AttributeError:
            ret_val["website_url"] = ""
        try:
            ret_val["download_url"] = dependency.download_url
        except AttributeError:
            ret_val["download_url"] = ""
        try:
            ret_val["download_dir"] = dependency.download_dir
        except AttributeError:
            ret_val["download_dir"] = ""
        try:
            ret_val["install_cmd"] = dependency.install_cmd
        except AttributeError:
            ret_val["install_cmd"] = ""
        try:
            ret_val["ok_if_exists"] = dependency.ok_if_exists
        except AttributeError:
            ret_val["ok_if_exists"] = ""
        try:
            ret_val["executable_check_regex"] = dependency.executable_check_regex
        except AttributeError:
            ret_val["executable_check_regex"] = ""
        try:
            ret_val["executable_argument"] = dependency.executable_argument
        except AttributeError:
            ret_val["executable_argument"] = ""
        try:
            ret_val["ok_if_executable"] = dependency.ok_if_executable
        except AttributeError:
            ret_val["ok_if_executable"] = ""
            ret_val["executable_argument"] = ""
            ret_val["executable_check_regex"] = ""
        ret_val["is_checked"] = "false"

        return ret_val


################################################################################
class ProjectDependency:
    """Parses the project dependency configuration file and checks the 
    dependencies.

    Parses the project dependency JSON file and saves the config file to 
    `dependency_cfg`. Checks the dependencies and tries to download and
    install missing dependencies. Writes the altered configuration to the JSON 
    file.
    
    Attributes:

        config_path (FilePath): path to the project dependency JSON file
        dependency_cfg (ProgDepConfig): the project dependency config object
    
    Methods:
            writeJSON: writes the changes to the project dependency 
                        configuration file
    
    """
    ###########################################################################
    def __init__(self, dependency_config:FilePath) -> None:
        """Parses the project dependency JSON configuration file.

        Stores the configuration in the attribute `dependency_cfg`.

        Args:
            dependency_config (FilePath): the configuration file of project dependencies to load
        """
        self.config_path = os.path.normpath(dependency_config)

        print("Parsing project dependency config file \"{path}\"".format(
            path=self.config_path))
        
        if not pathlib.Path(self.config_path).is_file(): 
            print("ERROR: project dependency config file \"{file}\" not found or is not a file!".format(
                file=self.config_path))
            sys.exit(EXT_ERR_LD_FILE)

        try:
            with io.open(self.config_path, mode= "r", encoding="utf-8") as file:
                tmp_cfg = json.load(file, object_hook=lambda dict: SimpleNamespace(**dict))

        except Exception as exp:
            print("ERROR: error \"{error}\" parsing file \"{path}\"".format(error=exp, path=self.config_path))
            sys.exit(EXT_ERR_LD_FILE)

        if tmp_cfg.file_name != PROJECT_DEP_FILE_NAME:
            print("ERROR: project dependency file \"{path}\" is not a valid project dependency file!".format(path=self.config_path))
            print("ERROR: the value of 'file_name' should be \"{should}\" but is \"{but_is}\""
                  .format(should=PROJECT_DEP_FILE_NAME, but_is=tmp_cfg.file_name))
            sys.exit(EXT_ERR_NOT_VLD)

        file_major, file_minor = tmp_cfg.file_version.split(sep=".")
        if file_major < CFG_VERSION.major or file_minor < CFG_VERSION.minor:
            print("ERROR: project dependency file \"{path}\" is not a valid project dependency file!".format(
                path=self.config_path))
            print("ERROR: project dependency file version (the value of 'file_version') is too old. is \"{old}\" should be \"{new}\""
                  .format(old=tmp_cfg.file_version, new=".".join(CFG_VERSION)))
            sys.exit(EXT_ERR_NOT_VLD)     
        
        self.dependency_cfg = ProjDepConfig(tmp_cfg)
        
    ############################################################################
    def checkDependencies(self, force_check: bool = False) -> None:
        """Runs all configured dependency checks.

        Checks for each dependency if the configured file exists or the 
        configured executable works. If not, it tries to download and/or install 
        the dependency and tries again.

        Args:
            force_check (bool, optional): if this is `True`, check the 
                        dependency even if it has been checked before - if 
                        `is_checked` is `True`. Defaults to False.
        """
        for dep in self.dependency_cfg.dependencies: 
            if dep["is_checked"] == "false" or force_check == True:                
                if not self.isDependencyFulfilled(dep): 
                    self.installDep(dep)
                    dep["is_checked"] = self.isDependencyFulfilled(dep)
            else:
                print("Project dependency \"{name}\" has already been checked OK".format(
                    dep["name"]))

        self.dependency_cfg.generated_at = datetime.datetime.now(
            tz=None).isoformat(sep=" ", timespec="seconds")

    ############################################################################
    def isDependencyFulfilled(self, dep: Dict[str, str]) -> bool:
        """Checks if the given dependency is installed.

        Checks if the configured path exist or the configured executable works.

        Args:
            dep (Dict[str, str]): the dependency dictionary to check

        Returns:
            bool: `True`, if the dependency has been found
                  `False` else 
        """
        print("Checking if dependency \"{name}\" is installed ...".format(
            name=dep["name"]))

        if dep["ok_if_exists"] != "":
            if pathlib.Path(dep["ok_if_exists"]).is_file() or pathlib.Path(dep["ok_if_exists"]).is_dir():
                print("Path \"{path}\" exists, dependency \"{name}\" is installed".format(
                    path=dep["ok_if_exists"], name=dep["name"]))
                dep["is_checked"] = True
                return True
            else:
                print("ERROR: Path \"{path}\" does not exist, dependency \"{name}\" not found!".format(
                    path=dep["ok_if_exists"], name=dep["name"]))
        
        if dep["ok_if_executable"] != "":
            print("Checking executable \"{exe}\"".format(
                exe=dep["ok_if_executable"]))
            dep["is_checked"] = self.isExecuteableDep(dep)
            if dep["is_checked"]:                
                return True

        print("ERROR: dependency \"{name}\" not found!".format(
            name=dep["name"]))
        dep["is_checked"] = False
        return False
    
    ############################################################################
    def installDep(self, dep: Dict[str, str]) -> None:
        """Download and/or install the given dependency.

        Args:
            dep (Dict[str, str]): the dependency to install or download
        """
        pass

    ############################################################################
    def isExecuteableDep(self, dep: Dict[str, str]) -> bool:
        """Execute the dependency, if that works, returns `True`.

        Args:
            dep (Dict[str, str]): the dependency to run

        Returns:
            bool: `True` if the executable has been running OK and returns the 
                         configured string.
                  `False` else
        """
        return False

    ############################################################################
    def writeJSON(self) -> None:
        """Writes the changes to the JSON file.
        """
        print("Writing project dependency configuration file \"{file}\"".format(
            file=self.config_path))

        self.dependency_cfg.file_version = ".".join(CFG_VERSION)

        with io.open(self.config_path, mode="w",) as json_file:
            try:
                json.dump(obj=self.dependency_cfg.__dict__, fp=json_file,
                          skipkeys=True, indent=4)
            except Exception as excp:
                print("ERROR: error \"{error}\" trying to write project dependency configuration to file \"{file}\""
                      .format(error=excp, file=self.config_path))
                sys.exit(EXT_ERR_WR_FILE)
    