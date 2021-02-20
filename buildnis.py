#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

import sys
import platform
from modules import EXT_ERR_IMP_MOD, EXT_ERR_PYTH_VERS

if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("ERROR: Python version is too old, I need at least Python 3.9, this has a version of {version}"
        .format(version=platform.python_version()), file=sys.stderr)
    sys.exit(EXT_ERR_PYTH_VERS)
try:   
    import os
    import logging
except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(
        error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)

try:
    from modules.helpers.logging import getProgramLogger  
    from modules.config import project_dependency
    from modules.helpers.commandline import parseCommandLine
    import modules.config.config as json_config
    import modules.config.host as host_config
    import modules.config.check as check_tools
    from modules import EXT_OK
    from modules.config import HOST_FILE_NAME
    from modules.config import BUILD_TOOL_CONFIG_NAME
except ImportError as exp:
    print("ERROR: error \"{error}\" importing own modules".format(
        error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)




################################################################################
def main():
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.
    """
    commandline_args = parseCommandLine()
    
    logger = getProgramLogger(commandline_args.log_level, commandline_args.log_file)
  
    logger.debug("Commandline arguments: \"{args}\"".format(args=commandline_args.__dict__))
    
    logger.info("Setting log level to \"{lvl}\"".format(
        lvl=logging.getLevelName(commandline_args.log_level)))

    logger.warning("Using project config \"{config}\"".format(
        config=commandline_args.project_config_file))

    project_cfg_dir = os.path.normpath(
        os.path.dirname(commandline_args.project_config_file))

    host_cfg = host_config.Host()
    
    host_cfg_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    host_cfg_filename = "_".join([host_cfg_filename, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])

    host_cfg.writeJSON(json_path=host_cfg_filename)         
   
    logger.debug("Host config: \"\"\"{cfg}\"\"\"".format(cfg=host_cfg))

    check_buildtools = check_tools.Check(os_name=host_cfg.os, arch=host_cfg.cpu_arch)
    
    if commandline_args.conf_dir == "" or commandline_args.conf_dir == None:
        build_tools_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    else:
        build_tools_filename = "/".join(
            [commandline_args.conf_dir, host_cfg.host_name])
    
    build_tools_filename = "_".join(
        [build_tools_filename, BUILD_TOOL_CONFIG_NAME])
    build_tools_filename = ".".join([build_tools_filename, "json"])
    check_buildtools.writeJSON(json_path=build_tools_filename)

    cfg = json_config.Config(project_config=commandline_args.project_config_file)

    project_dep_cfg = project_dependency.ProjectDependency(
        cfg.project_cfg.project_dependency_config) 

    project_dep_cfg.checkDependencies(force_check=True)

    project_dep_cfg.writeJSON()

    # print(cfg.project_cfg.__dict__)

    # print("=======================================================")

    # for module_key in cfg.module_cfgs:
    #     print(module_key, cfg.module_cfgs[module_key].__dict__)
    #     print("")

    #     print("=======================================================")

    #     for build_key in cfg.build_cfgs:
    #         print(build_key, cfg.build_cfgs[build_key].__dict__)
    #         print("")

    sys.exit(EXT_OK)

################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main()
