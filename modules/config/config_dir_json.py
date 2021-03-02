# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_dir_json.py
# Date:     02.Mar.2021
###############################################################################

from __future__ import annotations

import logging
import os

from modules.helpers.files import checkIfIsFile, makeDirIfNotExists
from modules.helpers import LOGGER_NAME
from modules.helpers.json import getJSONDict, readJSON, writeJSON
from modules.config import CFG_DIR_NAME, FilePath


class ConfigDirJson:
    """Class to handle the configuration of the directory all generated 
    configuration files are written to.

    Attributes:

        file_name (FilePath):  The path to the JSON configuration file
        cfg_path (FilePath): The directory to save generated configurations to
        _logger (logging.Logger): Logger instance to log messages to `stdout` 
                                    or file

    Methods:

        writeJSON: Writes the configuration directory configuration to a JSON 
                    file with path `file_name`.
    """

    ############################################################################
    def __init__(self, file_name: FilePath, working_dir: FilePath, cfg_path: FilePath = "") -> None:
        """Loads an existing configuration directory configuration if it exists, 
        or uses the given path from the command line argument `--generate-conf-dir`.

        Args:
            file_name (FilePath): The file name of the configuration directory configuration, should
                                    be something like `working_dir/CFG_DIR_NAME`
            working_dir (FilePath): path of the working directory, the directory the project config is
                                    located in (needed to find an existing configuration directory 
                                    configuration file)
            cfg_path (FilePath, optional): The path to the configuration directory. Defaults to "".
        """
        self.file_name = file_name
        self._logger = logging.getLogger(LOGGER_NAME)

        if cfg_path != "":
            if os.path.isabs(cfg_path):
                self.cfg_path = os.path.normpath(cfg_path)
            else:
                self.cfg_path = os.path.abspath(
                    "/".join([working_dir, cfg_path]))
        else:
            try:
                if checkIfIsFile(file_name) == False:
                    self.cfg_path = os.path.abspath(working_dir)
                else:
                    tmp_object = readJSON(
                        json_path=file_name, file_text="configuration directory", conf_file_name=CFG_DIR_NAME)
                    self.cfg_path = os.path.abspath(tmp_object.cfg_path)
            except Exception as excp:
                self._logger.critical("error \"{error}\" loading configuration directory configuration \"{path}\"".format(
                    error=excp, path=file_name))

        try:
            makeDirIfNotExists(self.cfg_path)
        except Exception as excp:
            self._logger.critical("error \"{error}\" trying to generate directory \"{path}\"".format(
                error=excp, path=cfg_path))

    ############################################################################
    def writeJSON(self) -> None:
        """Writes the path to the project config directory to a JSON file with 
        the given path `json_path`.      
        """
        try:
            writeJSON(getJSONDict(self), json_path=self.file_name,
                      file_text="configuration directory", conf_file_name=CFG_DIR_NAME)
        except Exception as excp:
            self._logger.critical("error \"\{error}\" trying to write configuration directory configuration \"{path}\"".format(
                error=excp, path=self.file_name))
