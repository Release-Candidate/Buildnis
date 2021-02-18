# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host.py
# Date:     15.Feb.2021
###############################################################################

import datetime
from modules import EXT_ERR_WR_FILE
from modules.config import AMD64_ARCH_STRING, FilePath, HOST_FILE_NAME, LINUX_OS_STRING, OSX_OS_STRING, WINDOWS_OS_STRING
import platform
import pprint
import json
import os
import io
import sys
import subprocess

class Host:
    """Holds all information about the host this is running on.

    Stores hostname, OS, OS version, CPU architecture, RAM, CPU name, ...

    Attributes:
        host_name:      This host's name
        os:             The OS this is running on (like "Windows", "Linux")
        os_vers_major:  Major version of the OS (like "10" for Windows 10)
        os_vers:        Excact version string
        cpu_arch:       CPU architecture, like "x64" or "x86"
        cpu:            The detailed name of the CPU
        file_name:      The JSON identifier of the host config file, part 
                        of the file name
        level2_cache:   Size of the CPU's level 2 cache, in bytes
        level3_cache:   Size of the CPU's level 3 cache, in bytes
        num_cores:      The number of physical cores
        num_logical_cores: The number of logical, 'virtual' cores
        ram_total:      Amount of physical RAM in bytes
        gpu:            The list of names of all GPUs
        python_version: The version of this host's Python interpreter
        json_path:      The path to the written JSON host config file

    Methods:
        writeJSON: saves the information to a JSON file.
        collectWindowsConfig: adds information, that has to be collected in a
                            Windows specific way
        collectLinuxConfig: adds information, that has to be collected in a
                            Linux specific way
        collectOSXConfig:   adds information, that has to be collected in a
                            Mac OS X specific way
    """
    ###########################################################################
    def __init__(self) -> None:
        """Constructor of class Host, gathers and sets the host's environment.

        Like OS, hostname, OS version, CPU architecture, ...
        """
        print("Gathering information about this host ...")

        self.file_name=HOST_FILE_NAME

        self.os, self.host_name, self.os_vers_major, self.os_vers, self.cpu_arch, self.cpu = platform.uname()
        if self.os == "Darwin":
            self.os = OSX_OS_STRING
        if self.cpu_arch == "AMD64" or self.cpu_arch == "x86_64":
            self.cpu_arch = AMD64_ARCH_STRING

        self.python_version = platform.python_version()

        if self.os == WINDOWS_OS_STRING:
            self.collectWindowsConfig()

        elif self.os == LINUX_OS_STRING:
            self.collectLinuxConfig()

        elif self.os == OSX_OS_STRING:
            self.collectOSXConfig()

        else:
            print("ERROR: error, \"{os_name}\" is a unknown OS!".format(os_name=self.os))
            print("You can add support of this OS to the file \"modules\config\host.py\"")
            print()

    ###########################################################################
    def __repr__(self) -> str:
        """Returns a string representing the object.

        Returns:
            str: A strings representation of the objects data
        """
        return pprint.pformat(vars(self))

    ###########################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the host's config to a JSON file

        Args:
            json_path (str):  the path to write the json file to
        """
        self.json_path = os.path.normpath(json_path)
        self.generated_at = datetime.datetime.now(
            tz=None).isoformat(sep=" ", timespec="seconds")
        print("Writing host configuration file \"{file}\"".format(file=self.json_path))

        with io.open(self.json_path,mode="w",) as json_file:
            try:
                json.dump(obj=self.__dict__,fp=json_file, skipkeys=True, indent=4)
            except Exception as excp:
                print("ERROR: error \"{error}\" trying to write host configuration to file \"{file}\""
                    .format(error=excp,file=self.json_path))
                sys.exit(EXT_ERR_WR_FILE)

    #############################################################################  
    def collectWindowsConfig(self) -> None:
        """Collect information about the hardware we're running on on Windows.

        Calls these commands and parses their outputs:

        wmic cpu get L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,NumberOfCores,Name
        wmic memorychip get capacity
        wmic path win32_VideoController get name
        """
        try:
            cpu_info_cmd = subprocess.run(
                ["wmic", "cpu", "get", "L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,NumberOfCores"], 
                capture_output=True, text=True, check=True, timeout=120)
            cpu_name_cmd = subprocess.run(
                ["wmic", "cpu", "get","Name"],
                capture_output=True, text=True, check=True, timeout=120)
            mem_info_cmd = subprocess.run(
                ["wmic", "memorychip", "get", "capacity"],
                capture_output=True, text=True, check=True, timeout=120)
            gpu_info_cmd = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get", "name"],
                capture_output=True, text=True, check=True, timeout=120)            
                 
            for line in cpu_info_cmd.stdout.strip().split("\n"):
                if "L2CacheSize" in line:
                    continue
                if line != "":
                    level2_cache, level3_cache, num_cores, num_logical_cores = line.split()
                    try:
                        self.level2_cache = int(level2_cache)
                        self.level3_cache = int(level3_cache)
                        self.num_cores = int(num_cores)
                        self.num_logical_cores = int(num_logical_cores)
                    except:
                        pass

            for line in cpu_name_cmd.stdout.strip().split("\n"):
                if "Name" in line:
                    continue
                if line != "":
                    self.cpu = line

            self.gpu = []
            for line in gpu_info_cmd.stdout.strip().split("\n"):
                if "Name" in line:
                    continue
                if line != "":
                    self.gpu.append(line.strip())

            self.ram_total = 0
            for line in mem_info_cmd.stdout.strip().split("\n"):
                if "Capacity" in line:
                    continue
                if line != "":
                    try:                    
                        self.ram_total += int(line)                        
                    except:
                        pass

        except subprocess.CalledProcessError as excp:
            print ("ERROR: error \"{error}\" calling wmic",format(error=excp))
        except Exception as excp2:
            print("ERROR: error \"{error}\" calling wmic".format(error=excp2))

    #############################################################################
    # grep "model name" /proc/cpuinfo |uniq
    # grep "cache size" /proc/cpuinfo |uniq
    # grep "cpu cores" /proc/cpuinfo |uniq
    # grep "siblings" /proc/cpuinfo |uniq
    # free -b|grep "Mem:"
    # grep "DISTRIB_DESCRIPTION" /etc/lsb-release
    # lspci|grep VGA
    def collectLinuxConfig(self) -> None:
        """Collect information about the hardware we're running on on Linux.

        Parses `/proc/cpuinfo`, the output of `free` and similar.
        """
        pass

    #############################################################################
    # sysctl -n hw.memsize
    # sysctl -n hw.physicalcpu
    # sysctl -n hw.logicalcpu
    # sysctl -n hw.l2cachesize
    # sysctl -n hw.l3cachesize
    # sysctl -n machdep.cpu.brand_string
    def collectOSXConfig(self) -> None:
        """Collect information about the hardware we're running on on MacOS X.


        """
        pass

################################################################################
def printHostInfo() -> None:
    """To test the collection of the host's information, print all to stdout.
    """
    print(Host())

################################################################################
if __name__ == '__main__':
    printHostInfo()


