#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

from buildnis.modules import EXT_ERR_IMP_MOD

try:
    import sys
    import os
    import pprint
    import logging
    import pathlib
    from typing import List, Tuple
except ImportError as exp:
    print('ERROR: error "{error}" importing modules'.format(error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)

try:
    from buildnis.modules.config.config_dir_json import ConfigDirJson
    from buildnis.modules.config import config_values
    from buildnis.modules.config import config
    from buildnis.modules.helpers.files import checkIfIsFile
    from buildnis.modules.config import PROJECT_FILE_NAME
    from buildnis.modules.helpers.logging import getProgramLogger
    from buildnis.modules.config import project_dependency
    from buildnis.modules.helpers.commandline import parseCommandLine
    from buildnis.modules.config import check
    from buildnis.modules.config.host import Host
    from buildnis.modules.config import FilePath, PROJECT_DEP_FILE_NAME
    from buildnis.modules import EXT_OK
    from buildnis.modules.config import HOST_FILE_NAME
    from buildnis.modules.config import BUILD_TOOL_CONFIG_NAME
    from buildnis.modules.helpers.commandline_arguments import CommandlineArguments
    from buildnis.modules.config import CFG_DIR_NAME
    from buildnis.modules.helpers.files import deleteDirs, deleteFiles
    from buildnis.modules.config.config_files import ConfigFiles, ConfigTuple
    from buildnis.modules.config.config import Config
except ImportError as exp:
    print(
        'ERROR: error "{error}" importing own modules'.format(error=exp),
        file=sys.stderr,
    )
    sys.exit(EXT_ERR_IMP_MOD)


################################################################################
def main():
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.
    """
    commandline_args, logger = setCmdLineArgsLogger()

    project_cfg_dir = commandline_args.conf_dir

    project_cfg_dir, config_dir_config = setUpConfDir(
        commandline_args, logger, project_cfg_dir
    )

    # Always create host config
    host_cfg, host_cfg_filename = setUpHostCfg(logger, project_cfg_dir)

    json_config_files = setUpPaths(
        project_cfg_dir=project_cfg_dir,
        host_cfg_file=host_cfg_filename,
        list_of_generated_files=config_values.g_list_of_generated_files,
        host_cfg=host_cfg,
    )

    if not commandline_args.do_clean:
        host_cfg.writeJSON(json_path=host_cfg_filename)
        config_values.g_list_of_generated_files.append(host_cfg_filename)

        if (
            not json_config_files.build_tools_cfg.exists
            or commandline_args.do_configure is True
        ):
            writeBuildTools(commandline_args, logger, host_cfg, json_config_files)

        else:
            logger.warning(
                'JSON file "{path}" already exists, not checking for build tool configurations'.format(
                    path=json_config_files.build_tools_cfg.path
                )
            )

        ifConfigureDeleteProjectJSON(commandline_args, logger, json_config_files)

        cfg = config.Config(
            project_config=commandline_args.project_config_file,
            json_path=json_config_files.project_cfg.path,
        )

        cfg.project_dep_cfg = project_dependency.ProjectDependency(
            cfg.project_dependency_config,
            json_path=json_config_files.project_dep_cfg.path,
        )

        cfg.expandAllPlaceholders()

        if (
            not json_config_files.project_dep_cfg.exists
            or commandline_args.do_configure is True
        ):
            cfg.checkDependencies(force_check=True)

        else:
            logger.warning(
                'JSON file "{path}" already exists, not checking project dependencies'.format(
                    path=json_config_files.project_dep_cfg.path
                )
            )
            cfg.checkDependencies(force_check=False)

        cfg.project_dep_cfg.writeJSON()

        if not json_config_files.project_dep_cfg.exists:
            config_values.g_list_of_generated_files.append(
                json_config_files.project_dep_cfg.path
            )

        logger.debug('Project config: """{cfg}"""'.format(cfg=cfg))
        logger.debug(
            'Project dependency config: """{cfg}"""'.format(cfg=cfg.project_dep_cfg)
        )

        writeProjectJSON(host_cfg_filename, json_config_files, cfg)

        config_dir_config.writeJSON()

    else:
        logger.warning(
            'Not doing anything but deleting files, a "clean" argument ("--clean" or "--distclean") has been given!'
        )

    # skipcq: FLK-E265
    #! WARNING: no more logging after this function!
    # Logger is shut down
    doDistClean(
        commandline_args=commandline_args,
        logger=logger,
        list_of_generated_files=config_values.g_list_of_generated_files,
        list_of_generated_dirs=config_values.g_list_of_generated_dirs,
    )

    sys.exit(EXT_OK)


################################################################################
def writeProjectJSON(
    host_cfg_filename: FilePath, json_config_files: ConfigFiles, cfg: Config
) -> None:
    """Writes the project configuration JSON to disk.

    Args:
        host_cfg_filename (FilePath): Path to the host configuration.
        json_config_files (ConfigFiles): The object holding the path to the project
                                        configuration JSON to write.
        cfg (Config): The project configuration instance to write to disk.
    """
    cfg.setBuildToolCfgPath(json_config_files.build_tools_cfg.path)
    cfg.setHostConfigPath(host_cfg_filename)
    cfg.writeJSON()
    if not json_config_files.project_cfg.exists:
        config_values.g_list_of_generated_files.append(json_config_files.project_cfg)


################################################################################
def ifConfigureDeleteProjectJSON(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    json_config_files: ConfigFiles,
) -> None:
    """Deletes the project configuration JSON if it exists and `--configure` has been
    called.

    Args:
        commandline_args (CommandlineArguments): The object holding the command line
                                                arguments
        logger (logging.Logger): THe logger to use.
        json_config_files (ConfigFiles): The path to the project configuration JSON and
                                            whether it exists.
    """
    if json_config_files.project_cfg.exists and commandline_args.do_configure is True:

        try:
            pathlib.Path(json_config_files.project_cfg).unlink()
            json_config_files.project_cfg.exists = False
        except Exception as excp:
            logger.error(
                'error "{error}" deleting generated project config file to reconfigure project'.format(
                    error=excp
                )
            )


################################################################################
def writeBuildTools(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    host_cfg: Host,
    json_config_files: ConfigFiles,
) -> None:
    """Writes the build tools configuration to disk.

    Args:
        commandline_args (CommandlineArguments): The object holding all command line
                                                    arguments.
        logger (logging.Logger): The logger to use.
        host_cfg (Host): The host configuration instance.
        json_config_files (ConfigFiles): Holds the Path to the build tools JSON
                                    configuration path, the path to write to.
    """
    check_buildtools = check.Check(
        os_name=host_cfg.os,
        arch=host_cfg.cpu_arch,
        user_path=commandline_args.conf_scripts_dir,
    )
    check_buildtools.writeJSON(json_path=json_config_files.build_tools_cfg.path)
    if not json_config_files.build_tools_cfg.exists:
        config_values.g_list_of_generated_files.append(
            json_config_files.build_tools_cfg.path
        )
    logger.debug('Build tool config: """{cfg}"""'.format(cfg=check_buildtools))


################################################################################
def setUpConfDir(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    project_cfg_dir: FilePath,
) -> Tuple[FilePath, ConfigDirJson]:
    """Sets up the configuration directory.

    Args:
        commandline_args ([CommandlineArguments]): instance holding the command line
                        parameters, especially `commandline_args.project_config_file`.
        logger ([type]): The `logger.Logger` instance to use.
        project_cfg_dir ([FilePath]): Path to the configuration directory.

    Returns:
        Tuple[FilePath, ConfigDirJson]: A Tuple containing the configuration directory
                                    and the `ConfigDirJson` instance to use.
    """
    working_dir = os.path.abspath(os.path.dirname(commandline_args.project_config_file))
    config_dir_filename = "/".join([working_dir, CFG_DIR_NAME])
    config_dir_filename = ".".join([config_dir_filename, "json"])
    config_dir_filename = os.path.abspath(config_dir_filename)
    config_dir_config = ConfigDirJson(
        file_name=config_dir_filename, working_dir=working_dir, cfg_path=project_cfg_dir
    )
    config_values.g_list_of_generated_files.append(config_dir_config.json_path)
    project_cfg_dir = config_dir_config.cfg_path
    if project_cfg_dir != working_dir:
        config_values.g_list_of_generated_dirs.append(project_cfg_dir)
    logger.info(
        'Setting project configuration directory to "{path}"'.format(
            path=project_cfg_dir
        )
    )
    return project_cfg_dir, config_dir_config


################################################################################
def setUpPaths(
    project_cfg_dir: FilePath,
    host_cfg_file: FilePath,
    list_of_generated_files: List[FilePath],
    host_cfg: Host,
) -> ConfigFiles:
    """Helper: set up all pathnames of JSON files.

    Args:
        project_cfg_dir (FilePath): The path to the directory the JSON files are
                                    generated in
        host_cfg (FilePath): The path to the generated host configuration JSON file
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (host_config.Host): host configuration object instance

    Returns:
        ConfigFiles: the paths to the JSON files and a bool that is `True` if the file
                     already has been created.
    """
    host_cfg_filename_exists = False
    try:
        if checkIfIsFile(host_cfg_file) is True:
            list_of_generated_files.append(host_cfg_file)
            host_cfg_filename_exists = True
    except:
        pass

    build_tools = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=BUILD_TOOL_CONFIG_NAME,
    )

    project_dep = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=PROJECT_DEP_FILE_NAME,
    )

    project_config = setUpConfigFile(
        project_cfg_dir=project_cfg_dir,
        list_of_generated_files=list_of_generated_files,
        host_cfg=host_cfg,
        config_name=PROJECT_FILE_NAME,
    )

    return ConfigFiles(
        host_cfg=ConfigTuple(path=host_cfg_file, exists=host_cfg_filename_exists),
        build_tools_cfg=build_tools,
        project_dep_cfg=project_dep,
        project_cfg=project_config,
    )


################################################################################
def setUpConfigFile(
    project_cfg_dir: FilePath,
    list_of_generated_files: List[FilePath],
    host_cfg: Host,
    config_name: str,
) -> ConfigTuple:
    """

    Args:
        project_cfg_dir (FilePath): The path to the directory the JSON files are
                                    generated in
        host_cfg (FilePath): The path to the generated host configuration JSON file
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (Host): host configuration object instance
        config_name (str): The name of the config file to return the path of.

    Returns:
        ConfigTuple: The path to the configuration JSON file and `True`, if
                                this file already exists, `False` if it will be
                                generated.
    """
    config_filename_exists = False
    config_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    config_filename = "_".join([config_filename, config_name])
    config_filename = ".".join([config_filename, "json"])
    config_filename = os.path.normpath(config_filename)
    try:
        if checkIfIsFile(config_filename) is True:
            list_of_generated_files.append(config_filename)
            config_filename_exists = True
    except:
        pass
    return ConfigTuple(path=config_filename, exists=config_filename_exists)


################################################################################
def doDistClean(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    list_of_generated_files: List[FilePath],
    list_of_generated_dirs: List[FilePath],
) -> None:
    """Helper: if argument `distclean` is set, delete all generated files.

    WARNING: Shuts down the logging mechanism, no more logging after this function!

    Args:
        commandline_args (object): Command line argument object instance
        logger (logging.Logger): The logger to use and stop
        list_of_generated_files (List[FilePath]): The list of files to delete
        list_of_generated_dirs (List[FilePath]): The list of directories to delete.
                            Attention: each directory must be empty!
    """
    deleteConfigs(
        commandline_args, logger, list_of_generated_files, list_of_generated_dirs
    )

    logging.shutdown()

    deleteLogfiles(commandline_args)


################################################################################
def deleteConfigs(
    commandline_args: CommandlineArguments,
    logger: logging.Logger,
    list_of_generated_files: List[FilePath],
    list_of_generated_dirs: List[FilePath],
):
    """Deletes all configuration files and directories.

    Args:
        commandline_args (object): Command line argument object instance
        logger (logging.Logger): The logger to use and stop
        list_of_generated_files (List[FilePath]): The list of files to delete
        list_of_generated_dirs (List[FilePath]): The list of directories to delete.
                            Attention: each directory must be empty!
    """
    if commandline_args.do_distclean is True:
        try:
            deleteFiles(logger, list_of_generated_files)
            deleteDirs(logger, list_of_generated_dirs)
        except Exception as excp:
            logger.error(
                'error "{error}" trying to delete a file ro directory'.format(
                    error=excp
                )
            )


################################################################################
def deleteLogfiles(commandline_args: CommandlineArguments) -> None:
    """Deletes the log file, if one has been configured from the command-line.

    Args:
        commandline_args (CommandlineArguments): Instance holding the command-line
                                arguments, to check, if a log file has been used.
    """
    try:
        if commandline_args.log_file != "" and commandline_args.log_file is not None:
            print(
                'distclean: trying to delete logfile "{name}"'.format(
                    name=commandline_args.log_file
                )
            )
            pathlib.Path(commandline_args.log_file).unlink(missing_ok=True)
    except Exception as excp:
        print(
            'ERROR: distclean: error "{error}" trying to delete log file "{name}"'.format(
                error=excp, name=commandline_args.log_file
            ),
            file=sys.sys.stderr,
        )


################################################################################
def setUpHostCfg(
    logger: logging.Logger,
    project_cfg_dir: FilePath,
) -> Tuple[Host, FilePath]:
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
    host_cfg = Host()

    host_cfg_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    host_cfg_filename = "_".join([host_cfg_filename, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])
    host_cfg_filename = os.path.normpath(host_cfg_filename)

    logger.debug('Host config: """{cfg}"""'.format(cfg=host_cfg))

    return host_cfg, host_cfg_filename


################################################################################
def setCmdLineArgsLogger() -> Tuple[CommandlineArguments, logging.Logger]:
    """Helper function: parses the command line, sets up the logger.

    Returns:
        Tuple[CommandLineArguments, logging.Logger]: The commandline object instance
                                                    and the logger instance to use
    """
    commandline_args = parseCommandLine()

    logger = getProgramLogger(commandline_args.log_level, commandline_args.log_file)

    pretty_args = pprint.pformat(commandline_args.__dict__, indent=4, sort_dicts=False)
    logger.debug('Commandline arguments: "{args}"'.format(args=pretty_args))

    logger.info(
        'Setting log level to "{lvl}"'.format(
            lvl=logging.getLevelName(commandline_args.log_level)
        )
    )

    logger.warning(
        'Using project config "{config}"'.format(
            config=commandline_args.project_config_file
        )
    )

    return commandline_args, logger


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main()
