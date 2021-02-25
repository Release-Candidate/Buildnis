#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

try:    
    import sys
    from modules import EXT_ERR_IMP_MOD
    import os
    import logging
    import pathlib
    from typing import List, Tuple
except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(
        error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)

try:
    from modules.config import PROJECT_FILE_NAME
    from modules.helpers.logging import getProgramLogger
    from modules.config import project_dependency
    from modules.helpers.commandline import parseCommandLine
    import modules.config.config as json_config
    import modules.config.host as host_config
    import modules.config.check as check_tools
    from modules.config.host import Host
    from modules.config import FilePath, PROJECT_DEP_FILE_NAME
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
    commandline_args, logger = setCmdLineArgsLogger()

    if commandline_args.conf_dir == "" or commandline_args.conf_dir == None:
        project_cfg_dir = os.path.normpath(
            os.path.dirname(commandline_args.project_config_file))
    else:
        project_cfg_dir = os.path.normpath(commandline_args.conf_dir)

    list_of_generated_files: List[FilePath] = []

    # Always create host config JSON
    host_cfg, host_cfg_filename = setUpHostCfg(
        list_of_generated_files, logger, project_cfg_dir)

    (build_tools_filename_exists, build_tools_filename,
     project_dep_filename_exists, project_dep_filename,
     project_config_filename_exists, project_config_filename) = setUpPaths(
        project_cfg_dir, list_of_generated_files, host_cfg)

    if build_tools_filename_exists == False or commandline_args.do_configure == True:
        check_buildtools = check_tools.Check(
            os_name=host_cfg.os, arch=host_cfg.cpu_arch)

        check_buildtools.writeJSON(json_path=build_tools_filename)
        if not build_tools_filename_exists:
            list_of_generated_files.append(build_tools_filename)
    else:
        logger.warning("JSON file \"{path}\" already exists, not checking for build tool configurations".format(
            path=build_tools_filename))

    if project_config_filename_exists == False or commandline_args.do_configure == True:
        cfg = json_config.Config(
            project_config=commandline_args.project_config_file)

        if not project_config_filename_exists:
            list_of_generated_files.append(project_config_filename)
    else:
        cfg = json_config.Config(
            project_config=project_config_filename)

    cfg.setBuildToolCfgPath(build_tools_filename)
    cfg.setHostConfigPath(host_cfg_filename)

    project_dep_cfg = project_dependency.ProjectDependency(
        cfg.project_cfg.project_dependency_config)

    if project_dep_filename_exists == False or commandline_args.do_configure == True:

        project_dep_cfg.checkDependencies(force_check=True)

    else:
        logger.warning("JSON file \"{path}\" already exists, not checking project dependencies".format(
            path=project_dep_filename))
        project_dep_cfg.checkDependencies(force_check=False)

    project_dep_cfg.writeJSON(project_dep_filename)

    if not project_dep_filename_exists:
        list_of_generated_files.append(project_dep_filename)

    cfg.setProjDepCfgPath(project_dep_filename)

    cfg.writeJSON(project_config_filename)
    if not project_config_filename_exists:
        list_of_generated_files.append(project_config_filename)

    # print(cfg.project_cfg.__dict__)

    # print("=======================================================")

    # for module_key in cfg.module_cfgs:
    #     print(module_key, cfg.module_cfgs[module_key].__dict__)
    #     print("")

    #     print("=======================================================")

    #     for build_key in cfg.build_cfgs:
    #         print(build_key, cfg.build_cfgs[build_key].__dict__)
    #         print("")

    #! WARNING: no more logging after this function!
    # Logger is shut down
    doDistClean(commandline_args, logger, list_of_generated_files)

    sys.exit(EXT_OK)

################################################################################


def setUpPaths(project_cfg_dir: FilePath, list_of_generated_files: List[FilePath], host_cfg: host_config.Host) -> Tuple[bool, FilePath, bool, FilePath, bool, FilePath]:
    """Helper: set up all pathnames of JSON files.

    Args:
        project_cfg_dir (): The path to the directory the JSON files are generated in
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (host_config.Host): host configuration object instance

    Returns:
        Tuple[bool, FilePath, bool, FilePath, bool, FilePath]: the paths to the JSON 
            files and a bool that is `True` if the file already has been created.
    """
    build_tools_filename_exists = False

    build_tools_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    build_tools_filename = "_".join(
        [build_tools_filename, BUILD_TOOL_CONFIG_NAME])
    build_tools_filename = ".".join([build_tools_filename, "json"])
    build_tools_filename = os.path.normpath(build_tools_filename)

    try:
        if pathlib.Path(build_tools_filename).is_file():
            list_of_generated_files.append(build_tools_filename)
            build_tools_filename_exists = True
    except:
        pass

    project_dep_filename_exists = False

    project_dep_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    project_dep_filename = "_".join(
        [project_dep_filename, PROJECT_DEP_FILE_NAME])
    project_dep_filename = ".".join([project_dep_filename, "json"])
    project_dep_filename = os.path.normpath(project_dep_filename)

    try:
        if pathlib.Path(project_dep_filename).is_file():
            list_of_generated_files.append(project_dep_filename)
            project_dep_filename_exists = True
    except:
        pass

    project_config_filename_exists = False

    project_config_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    project_config_filename = "_".join(
        [project_config_filename, PROJECT_FILE_NAME])
    project_config_filename = ".".join([project_config_filename, "json"])
    project_config_filename = os.path.normpath(project_config_filename)

    try:
        if pathlib.Path(project_config_filename).is_file():
            list_of_generated_files.append(project_config_filename)
            project_config_filename_exists = True
    except:
        pass

    return (build_tools_filename_exists, build_tools_filename,
            project_dep_filename_exists, project_dep_filename,
            project_config_filename_exists, project_config_filename)

################################################################################


def doDistClean(commandline_args: object, logger: logging.Logger, list_of_generated_files: List[FilePath]) -> None:
    """Helper: if argument `distclean` is set, delete all generated files.

    WARNING: Shuts down the logging mechanism, no more logging after this function!

    Args:
        commandline_args (object): command line argument object instance
        logger (logging.Logger): the logger to use and stop
        list_of_generated_files (List[FilePath]): 
    """
    if commandline_args.do_distclean == True:
        try:
            for file_path in list_of_generated_files:
                logger.warning(
                    "distclean: deleting file \"{name}\"".format(name=file_path))
                pathlib.Path(file_path).unlink(missing_ok=True)
        except Exception as excp:
            logger.error(
                "error \"{error}\" trying to delete file \"{name}\"".format(error=excp, name=file_path))

    logging.shutdown()

    try:
        if commandline_args.log_file != "" and commandline_args.log_file != None:
            print("distclean: trying to delete logfile \"{name}\"".format(
                name=commandline_args.log_file))
            pathlib.Path(commandline_args.log_file).unlink(missing_ok=True)
    except Exception as excp:
        print("ERROR: distclean: error \"{error}\" trying to delete log file \"{name}\"".format(
            error=excp, name=commandline_args.log_file), file=sys.sys.stderr)

################################################################################


def setUpHostCfg(list_of_generated_files: List[FilePath], logger: logging.Logger, project_cfg_dir: FilePath) -> Tuple[Host, FilePath]:
    """Helper: Sets up the host's configuration.

    Is always generated.

    Args:
        list_of_generated_files (List[FilePath]): The list of generated files to add to
        logger (logging.Logger): The logger to use
        project_cfg_dir (FilePath): Path to the project config JSON file

    Returns:
        Tuple[Host, FilePath]: the host configuration object instance and the host 
                    configuration's filename as a tuple
    """
    host_cfg = host_config.Host()

    host_cfg_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    host_cfg_filename = "_".join([host_cfg_filename, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])
    host_cfg_filename = os.path.normpath(host_cfg_filename)

    host_cfg.writeJSON(json_path=host_cfg_filename)

    list_of_generated_files.append(host_cfg_filename)

    logger.debug("Host config: \"\"\"{cfg}\"\"\"".format(cfg=host_cfg))

    return host_cfg, host_cfg_filename

################################################################################


def setCmdLineArgsLogger() -> Tuple[object, logging.Logger]:
    """Helper function: parses the command line, sets up the logger.  

    Returns:
        Tuple[object, logging.Logger]: The commandline object instance and the 
        logger instance to use
    """
    commandline_args = parseCommandLine()

    logger = getProgramLogger(
        commandline_args.log_level, commandline_args.log_file)

    logger.debug("Commandline arguments: \"{args}\"".format(
        args=commandline_args.__dict__))

    logger.info("Setting log level to \"{lvl}\"".format(
        lvl=logging.getLevelName(commandline_args.log_level)))

    logger.warning("Using project config \"{config}\"".format(
        config=commandline_args.project_config_file))

    return commandline_args, logger


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main()
