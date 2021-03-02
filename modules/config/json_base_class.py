# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     json_base_class.py
# Date:     02.Mar.2021
###############################################################################

from __future__ import annotations

import pprint
import logging
import sys
from typing import List

from modules.helpers.config_parser import parseConfigElement
from modules import EXT_ERR_LD_FILE
from modules.helpers.json import getJSONDict, readJSON, writeJSON
from modules.config import CFG_VERSION, FilePath
from modules.helpers import LOGGER_NAME


class JSONBaseClass:
    """Base class for all objects that read and/or write JSON configuration 
    files. 
    Holds the values of the JSON file in it'S attributes (all except 
    `_logger`, the `loggin.Logger` instance).

    Methods:
        expandAllPlaceholders: Replaces all placeholders (like `${PLACEHOLDER}`)
                                in the instance's attribute values.
        readJSON: Reads the JSON config file and saves the values to attributes.
        writeJSON: Writes the attributes and their values to the JSON file.
    """

    ###########################################################################
    def __init__(self, config_file_name: str, config_name: str) -> None:
        """Sets the config file's name to `config_file_name` and the internal
        file name to `config_name`.

        Args:
            config_file_name (str): [description]
            config_name (str): [description]
        """
        self.file_name = config_file_name
        self.name = config_name
        self.file_version = ".".join(CFG_VERSION)
        self._logger = logging.getLogger(LOGGER_NAME)

    ############################################################################
    def readJSON(self, json_path: FilePath) -> None:
        """Reads a JSON file and puts it's items into attributes of this object.

        Args:
            json_path (FilePath): The path of the JSON file to load.
        """
        try:
            tmp_obj = readJSON(json_path=json_path,
                               file_text=self.name, config_file_name=self.file_name)

            for item in tmp_obj.__dict__:
                if isinstance(item, str):
                    setattr(self, item, tmp_obj.__dict__[item])
                else:
                    self._logger.error(
                        "error reading file \"{file}\": found item \"{item}\" in object dictionary that isn't a string!".format(file=json_path, item=item))
        except Exception as excp:
            self._logger.critical(
                "error \"{error}\" reading JSON file \"{json_path}\"".format(error=excp, json_path=json_path))
            sys.exit(EXT_ERR_LD_FILE)

    ############################################################################
    def expandAllPlaceholders(self, parents: List[object]) -> None:
        """Goes through all configurations and replaces placeholders in their
        elements. A Placeholder is a string like `${PLACEHOLDER}`, a dollar
        sign followed by a curly opening brace, the string to replace and the 
        closing curly brace. 

        See also: `modules.helpers.config_parser.parseConfigElement`

        Args:
            parents (List[object]): The hierarchical list of parent objects.
        """
        local_parents = parents.copy()
        local_parents.append(self)
        tmp_obj = parseConfigElement(element=self, parents=local_parents)

        for item in tmp_obj.__dict__:
            if isinstance(item, str):
                setattr(self, item, tmp_obj.__dict__[item])
            else:
                self._logger.error(
                    "error expanding placeholders of file \"{file}\": found item \"{item}\" in object dictionary that isn't a string!".format(file=self.name, item=item))

    ############################################################################
    def writeJSON(self, json_path: FilePath) -> None:
        """Writes the class instance to the JSON file.

        Args:
            json_path (FilePath): the path to the file to write the JSON to
        """
        self.json_path = json_path
        writeJSON(getJSONDict(self.dependency_cfg), json_path=json_path,
                  file_text=self.name, conf_file_name=self.file_name)

    ###########################################################################
    def hasConfigChanged(self) -> bool:
        """[summary]

        Returns:
            bool: `True` if the original JSON file has changed since the time
                    the files checksum has been saved.
                   `False` else
        """
        ret_val = False

        try:
            ret_val = self.orig_file.isSame(self.)
        except:
            return ret_val

        return ret_val

    ###########################################################################
    def __repr__(self) -> str:
        """Returns a string representing the JSON object.

        Returns:
            str: A strings representation of the object's data
        """
        return "{name}:\n{config}".format(name=self.name, config=pprint.pformat(
            getJSONDict(self), indent=4, sort_dicts=False))
