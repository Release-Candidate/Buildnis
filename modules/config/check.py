# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     check.py
# Date:     16.Feb.2021
###############################################################################

import json
from modules import EXT_ERR_DIR, EXT_ERR_WR_FILE
import os
import io
from modules.config import Arch, BUILD_TOOL_CONFIG_NAME, CONFIGURE_SCRIPTS_PATH, FilePath, OSName
import pathlib
import sys
import subprocess
import pprint
from types import SimpleNamespace

class BuildToolCfg:
    """Helper class to encode Check.build_tools_cfgs to JSON.
    """
    def __init__(self, src: object) -> None:
        self.name = src.name
        self.name_long = src.name_long
        self.version = src.version
        self.build_tool_exe = src.build_tool_exe
        self.install_path = src.install_path
        self.env_script = src.env_script   
  

class WriteCfg:
    """Helper class to encode Check.build_tools_cfgs to JSON.
    """
    def __init__(self, json_path: FilePath, cfg_list: list) -> None: 
        
        self.file_name = json_path
        self.build_tool_cfgs = []

        for cfg in cfg_list:            
            temp_dict = dict()
            temp_dict["name"] = cfg.name
            temp_dict["name_long"] = cfg.name_long
            temp_dict["version"] = cfg.version
            temp_dict["build_tool_exe"] = cfg.build_tool_exe
            temp_dict["install_path"] = cfg.install_path
            temp_dict["env_script"] = cfg.env_script
            self.build_tool_cfgs.append(temp_dict)

  
        
  

class Check:
    """Checks if all build tools are present.
    
    Runs all build tool script_paths in `configure_script_paths` in the subdirectory 
    with the name of the OS passed to the constructor.

    Each build tool configuration (item of build_tool_cfgs) has the following 
    attributes:

    * `name`
    * `name_long`
    * `version`
    * `build_tool_exe`
    * `install_path`
    * `env_script`

    Attributes:
        os_name (OSName): the OS we are building for
        arch (Arch): the CPU architecture we are building for
        build_tool_cfgs: the list of build tool configurations returned from 
                        the script_paths in `configure_script_paths/OS`

    Methods:
        writeJSON: writes the gathered build tool configurations to the given 
                    JSON config file.
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

        working_dir = pathlib.Path(os.path.normpath(
            "/".join([CONFIGURE_SCRIPTS_PATH, os_name])))
        if not working_dir.is_dir(): 
            print("ERROR: \"\{path}\" does not exist or is not a directory!".format(path=working_dir))
            sys.exit(EXT_ERR_DIR)
        
        self.build_tool_cfgs = []
        for script_path in working_dir.glob("*"): 
            if script_path.is_file():
                print("Calling build tool config script \"{path}\"".format(path=script_path))
                try:
                    script_out = subprocess.run(
                        [script_path, self.arch],
                        capture_output=True, text=True, check=True, timeout=120)                 

                    build_tool_cfg = json.loads(
                        script_out.stdout, object_hook=lambda dict: SimpleNamespace(**dict))

                except subprocess.CalledProcessError as excp1:
                    print("ERROR: error \"{error}\" running build tool script \"{path}\""
                          .format(error=excp1, path=script_path))
                except Exception as excp:
                    print("ERROR: error \"{error}\" running build tool script \"{path}\""
                            .format(error=excp, path = script_path))             
               
                for item in build_tool_cfg.build_tools:
                    self.build_tool_cfgs.append(item)
      

    ############################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the gathered build tool configurations to a file.
        
        Args:
            json_path (FilePath): path to write the JSON build tools configuration to
        """
        self.json_path = os.path.normpath(json_path)
        print("Writing host configuration file \"{file}\"".format(
            file=self.json_path))

        write_cfg = WriteCfg(BUILD_TOOL_CONFIG_NAME, self.build_tool_cfgs)

        print(write_cfg.__dict__)
        with io.open(self.json_path, mode="w",) as json_file:
            try:                
                json.dump(obj=write_cfg.__dict__, fp=json_file,
                          skipkeys=True, indent=4)
            except Exception as excp:
                print("ERROR: error \"{error}\" trying to write build tool configurations to file \"{file}\""
                      .format(error=excp, file=self.json_path))
                sys.exit(EXT_ERR_WR_FILE)
        



    
