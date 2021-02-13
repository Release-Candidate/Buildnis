#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

import sys
import platform

if sys.version_info.major < 3 or sys.version_info.minor < 9:
    print("ERROR: Python version is too old, I need at least Python 3.9, this has a version of {version}"
        .format(version=platform.python_version()))
    sys.exit(3)

try:
    import getopt, pathlib, typing

except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(3)

try:
    import modules.config.config as json_config
except ImportError as exp:
    print("ERROR: error \"{error}\" importing modules".format(error=exp))
    sys.exit(3)


CommandlineArguments = typing.Dict

DEFAULT_CONFIG_FILE="./project_config.json"

################################################################################
def printUsage() -> None:
    '''
    Prints usage information about this program to stdout.
    '''
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
    '''
    Parses the command line arguments.

    Parses the command line arguments, exits the program if an illegal argument
    has been given.

    Parameters: 
    arguments: the command line arguments passed to the program

    Returns: 
    a dictionary of command line arguments.
    ["Config"] holds the path to the project's JSON configuration
    '''
    try:
        opts, args = getopt.getopt(arguments, "h", ["help"])
    except getopt.GetoptError as excp:
        print("ERROR: error parsing comandline: \"{error}\"".format(error=excp))
        print("")
        printUsage()
        sys.exit(1)
    
    ret_val={}
    ret_val["Config"] = DEFAULT_CONFIG_FILE

    for option, argument in opts:
        print("Option: {option} Argument: {argument}".format(option=option,argument=argument))

        if option in ("-h", "--help"):
            printUsage()
            sys.exit(0)

    if len(args) > 1:
        print("ERROR: more than one argument given!")
        print("")
        printUsage()
        sys.exit(1)

    for argument in arguments:       
        ret_val["Config"] = argument

    if not pathlib.Path(ret_val["Config"]).is_file():
        print("ERROR: configuration file \"{config}\" not found or is not a file!"
                .format(config=ret_val["Config"]))
        print("")
        printUsage()
        sys.exit(2)

    return ret_val

################################################################################
def main(arguments):
    '''
    Main entry point of Buildnis.

    Parses commandline arguments and runs the program.

    Parameters:
    arguments: the command line arguments passed to the program
    '''
    commandline_dict = parseCommandLine(arguments)
    print("Using project config \"{config}\"".format(config=commandline_dict["Config"]))

    cfg = json_config.Config(commandline_dict["Config"])
    


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
