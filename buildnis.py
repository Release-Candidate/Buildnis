#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations

from modules.config import FilePath
import sys
from modules import EXT_ERR_IMP_MOD, EXT_ERR_PYTH_VERS, VERSION


if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("ERROR: Python version is too old, I need at least Python 3.9, this has a version of {version}"
        .format(version=platform.python_version()))
    sys.exit(EXT_ERR_PYTH_VERS)
try:
    import argparse
    import pathlib
    from typing import List
    import platform    

except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(EXT_ERR_IMP_MOD)

try:
    import modules.config.config as json_config
    import modules.config.host as host_config
    import modules.config.check as check_tools
    from modules import EXT_ERR_LD_FILE, EXT_OK
    from modules.config import HOST_FILE_NAME
    from modules.config import BUILD_TOOL_CONFIG_NAME
except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(EXT_ERR_IMP_MOD)


DEFAULT_CONFIG_FILE = "./project_config.json"

class CommandlineArguments:
    """Holds information about the command line arguments passed to the program.

    Its attributes are the possible command line arguments of the program.

    Attributes:

        project_config_file (FilePath): the path to the project config file to 
                                        use
        do_configure (bool): 
        do_build (bool):
        build_targets (List[str]):
        do_check_what_to_do (bool):
    """
    ############################################################################
    def __init__(self, src: object) -> None:
        """Initializes all attributes to a sane default value.

        Args:
            src (object): the object to use to fill the values of the command 
                            line argument instance
        """
        try:
            self.project_config_file: FilePath = src.project_config_file
        except AttributeError:
            self.project_config_file: FilePath = DEFAULT_CONFIG_FILE
        try:
            self.do_configure: bool = src.do_configure
        except AttributeError:
            self.do_configure: bool = False
        try:
            self.do_build: bool = src.do_build
        except AttributeError:
            self.do_build: bool = False
        try:
            self.do_install: bool = src.do_install
        except AttributeError:
            self.do_install: bool = False
        try:
            self.do_clean: bool = src.do_clean
        except AttributeError:
            self.do_clean: bool = False
        try:
            self.build_targets: List(str) = src.build_targets
        except AttributeError:
            self.build_targets: List(str) = None
        try:
            self.install_targets: List(str) = src.install_targets
        except AttributeError:
            self.install_targets: List(str) = None
        
        self.do_check_what_to_do: bool = False

        self.checkTargetArgs(name="build_targets")

        self.checkTargetArgs(name="install_targets")

    ############################################################################
    def checkTargetArgs(self, name: str) -> None:
        """Checks the list stored in the attribute with the given name and 
        flattens it to a single list if it contains another list.

        Args:
            name (str): the name of the attribute to check the stored list of
        """
        tmp_targets = []
        if getattr(self, name) != None and getattr(self, name) != []:
            for target in getattr(self, name):
                if target != []:
                    if isinstance(target, List):
                        for sub_target in target:
                            tmp_targets.append(sub_target)
                    else:
                        tmp_targets.append(target)
            setattr(self, name, tmp_targets)
    

################################################################################
def parseCommandLine() -> CommandlineArguments:
    """Parses the command line arguments.

    Parses the command line arguments, exits the program if an illegal argument
    has been given.

    Parameters: 
        arguments: the command line arguments passed to the program

    Returns: 
       an `CommandlineArguments` instance containing the command line arguments as attributes.
    """
    cmd_line_parser = argparse.ArgumentParser(
        description="Buildnis is a build system used to build software.", 
        epilog="See website https://github.com/Release-Candidate/Buildnis for a detailed description.")

    cmd_line_parser.add_argument(
        "--version", action="version", version="Buildnis {version}".format(version=VERSION))

    cmd_line_parser.add_argument("project_config_file", metavar="PROJECT_CONFIG_FILE", nargs="?",
                                 help="path to the project config JSON file to use for the build. If no file is given, the default: \"{default_config}\" is used"
                                 .format(default_config=DEFAULT_CONFIG_FILE), default=DEFAULT_CONFIG_FILE)
    
    phase_group = cmd_line_parser.add_argument_group(
        "Phases of the build", "Only run one of the phases of a full build.")
    
    phase_group.add_argument("--configure", help="Configure the project.", default=False, action="store_true", dest="do_configure")
    phase_group.add_argument(
        "--build", help="Build the project. If a list of targets is given, these targets are build. The default is to build the default target.", 
        nargs="*", dest="build_targets", metavar="TARGET", action="append")
    phase_group.add_argument(
        "--install", help="Install the given targets. If no target is given, installs the project's default target.",
        dest="install_targets", metavar="TARGET", nargs="*", action="append")
    phase_group.add_argument(
        "--clean", help="Clean the project. Deletes all generated files and directories", 
        default=False, action="store_true", dest="do_clean")
       
    cmdline_args = cmd_line_parser.parse_args()

    return checkCmdLineArgs(cmd_line_parser, cmdline_args)

################################################################################
def checkCmdLineArgs(cmd_line_parser: argparse.ArgumentParser, cmdline_args: object) -> CommandlineArguments:
    """[summary]

    Args:
        cmd_line_parser (argparse.ArgumentParser): the `argparse.ArgumentParser` instance to use
        cmdline_args (object): the object returned by `cmd_line_parser.parse_args`

    Returns:
        CommandlineArguments: the checked and filled `CommandlineArguments` instance
    """
    ret_val = CommandlineArguments(cmdline_args)

    if ret_val.build_targets == None:
        ret_val.do_build = False
        ret_val.build_targets = []
    else:
        ret_val.do_build = True

    if ret_val.install_targets == None:
        ret_val.do_install = False
        ret_val.install_targets = []
    else:
        ret_val.do_install = True
        
    if ret_val.do_configure == False and ret_val.do_build == False and ret_val.do_install == False:
        ret_val.do_check_what_to_do = True
    
    if not pathlib.Path(ret_val.project_config_file).is_file():
        cmd_line_parser.print_help(file=sys.stderr)
        print("", file=sys.stderr)
        cmd_line_parser.exit(status=EXT_ERR_LD_FILE, message="ERROR: configuration file \"{config}\" not found or is not a file!"
                                     .format(config=ret_val.project_config_file))
        
    return ret_val

################################################################################
def main():
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.
    """
    commandline_args = parseCommandLine()
    print("Using project config \"{config}\"".format(config=commandline_args.project_config_file))

    host_cfg = host_config.Host()
    
    host_cfg_filename = "_".join([host_cfg.host_name, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])

    host_cfg.writeJSON(json_path=host_cfg_filename)         
   
    # print(host_cfg)

    check_buildtools = check_tools.Check(os_name=host_cfg.os, arch=host_cfg.cpu_arch)
    
    build_tools_filename = "_".join([host_cfg.host_name, BUILD_TOOL_CONFIG_NAME])
    build_tools_filename = ".".join([build_tools_filename, "json"])
    check_buildtools.writeJSON(json_path=build_tools_filename)

    cfg = json_config.Config(project_config=commandline_args.project_config_file)

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
