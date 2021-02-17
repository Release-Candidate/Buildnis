#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from modules.config import BUILD_TOOL_CONFIG_NAME
import sys
from modules import EXT_ERR_IMP_MOD, EXT_ERR_PYTH_VERS


if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("ERROR: Python version is too old, I need at least Python 3.9, this has a version of {version}"
        .format(version=platform.python_version()))
    sys.exit(EXT_ERR_PYTH_VERS)

try:
    import getopt
    import pathlib
    import typing
    import platform

except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(EXT_ERR_IMP_MOD)

try:
    import modules.config.config as json_config
    import modules.config.host as host_config
    import modules.config.check as check_tools
    from modules import EXT_ERR_CMDLINE, EXT_ERR_LD_FILE, EXT_OK
    from modules.config import HOST_FILE_NAME
except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(EXT_ERR_IMP_MOD)


CommandlineArguments = typing.Dict

DEFAULT_CONFIG_FILE="./project_config.json"

################################################################################
def printUsage() -> None:
    """Prints usage information about this program to stdout.
    """
    usage_string = """Usage: buildnis.py [-h|--help] PROJECT_CONFIG

Buildnis is a build system used to build software.

Options:
    -h|--help   show this information and exit

Arguments: 
    PROJECT_CONFIG  path to the project config JSON file to use for the build.
                    Default: {default_config}
""" .format(default_config=DEFAULT_CONFIG_FILE)
    print(usage_string)

################################################################################
def parseCommandLine(arguments) -> CommandlineArguments:
    """Parses the command line arguments.

    Parses the command line arguments, exits the program if an illegal argument
    has been given.

    Parameters: 
        arguments: the command line arguments passed to the program

    Returns: 
        a dictionary of command line arguments.
        ["Config"] holds the path to the project's JSON configuration
    """
    try:
        opts, args = getopt.getopt(arguments, "h", ["help"])
    except getopt.GetoptError as excp:
        print("ERROR: error parsing comandline: \"{error}\"".format(error=excp))
        print("")
        printUsage()
        sys.exit(EXT_ERR_CMDLINE)
    
    ret_val={}
    ret_val["Config"] = DEFAULT_CONFIG_FILE

    for option, argument in opts:
        print("Option: {option} Argument: {argument}".format(option=option,argument=argument))

        if option in ("-h", "--help"):
            printUsage()
            sys.exit(EXT_OK)

    if len(args) > 1:
        print("ERROR: more than one argument given!")
        print("")
        printUsage()
        sys.exit(EXT_ERR_CMDLINE)

    for argument in arguments:       
        ret_val["Config"] = argument

    if not pathlib.Path(ret_val["Config"]).is_file():
        print("ERROR: configuration file \"{config}\" not found or is not a file!"
                .format(config=ret_val["Config"]))
        print("")
        printUsage()
        sys.exit(EXT_ERR_LD_FILE)

    return ret_val

################################################################################
def main(arguments):
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.

    Parameters:
    arguments: the command line arguments passed to the program
    """
    commandline_dict = parseCommandLine(arguments=arguments)
    print("Using project config \"{config}\"".format(config=commandline_dict["Config"]))

    host_cfg = host_config.Host()
    
    host_cfg_filename = "_".join([host_cfg.host_name, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])

    host_cfg.writeJSON(json_path=host_cfg_filename)         
   
    # print(host_cfg)

    check_buildtools = check_tools.Check(os_name=host_cfg.os, arch=host_cfg.cpu_arch)
    
    build_tools_filename = "_".join([host_cfg.host_name, BUILD_TOOL_CONFIG_NAME])
    build_tools_filename = ".".join([build_tools_filename, "json"])
    check_buildtools.writeJSON(json_path=build_tools_filename)

    cfg = json_config.Config(project_config=commandline_dict["Config"])

    # print(cfg.project_cfg.__dict__)

    # print("=======================================================")

    # for module_key in cfg.module_cfgs:
    #     print(module_key, cfg.module_cfgs[module_key].__dict__)
    #     print("")

    #     print("=======================================================")

    #     for build_key in cfg.build_cfgs:
    #         print(build_key, cfg.build_cfgs[build_key].__dict__)
    #         print("")



################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
