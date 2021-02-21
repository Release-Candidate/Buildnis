# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     files.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations

from modules import BuildnisException
from modules.config import FilePath
import os
import pathlib
import hashlib

class FileCompareException(BuildnisException):
    """Exception raised if a given file path can't be accessed or read to 
    generate the hash.
    """
    pass

class FileCompare:
    """Holds information about a file to compare it to another version of itself
    to see if something has changed.

    Does the following to steps:
        * compares the file sizes, if they are the same
        * compares the Blake2 hashes of both files

    Attributes:

        path (FilePath): path to the file as string
        path_obj (pathlib.Path): the `Path` object of the file
        size (int): the size of the file in bytes (symlinks don't have a 
                    meaningful size)
        hash (str): the BLAKE2 hash of the file's contend as a hex string.

    Methods:

        isSame (bool): returns true if `self` 'is' the same as the given file.
        generateHash (str): generates the hash of the file, saves it in 
                         `hash` and returns it   
    """

    ############################################################################
    def __init__(self, file: FilePath) -> None:
        """Initializes the `FileCompare` object using it's path.

        If the given path `file` isn't a file or is not accessible, an exception
        of type `FileCompareException` is thrown.

        Raises:
            FileCompareException: if something goes wrong

        Args:
            file (FilePath): The path to the file.
        """
        try:
            self.path = os.path.abspath(file)

            self.path_obj = pathlib.Path(self.path)

            if not self.path_obj.is_file():
                raise FileCompareException(
                    "file \"{path}\" does not exist or is not a file!".format(path=self.path))

            self.size = self.path_obj.stat().st_size

            self.hash = hashFile(self.path)
            
        except Exception as excp:
            raise FileCompareException (excp)

    ############################################################################
    def generateHash(self) -> str:
        """Rehashes the file, saves and returns the hash as hex string.

        The hash replaces the old one in the attribute `hash`.

        Raises:
            FileCompareException: if something goes wrong

        Returns:
            str: The hash of the file with path `path` as hex string.
        """
        return hashFile(self.path)

    ############################################################################
    def isSameFile(self, other: FileCompare) -> bool:
        """Checks whether two `FileComare` instances hold the same file content.

        
        Compares `self` against another FileCompare instance, comparing file size
        and hash.

        Returns `True` if both files have the same content.

        Attention: does NOT compare the filenames, only file size and hash of the 
        files are compared.

        Args:
            other (FileCompare): the instance to compare `self` to

        Raises:
            FileCompareException: if something doesn't work out well ....

        Returns:
            bool: `True`, if both instances have the same filesize and hash.
                  `False` else
        """
        if self.size == other.size and self.hash == other.hash:
            return True
        else:
            return False 

    ############################################################################
    def isSame(self, file: FilePath) -> bool:
        """Checks whether `self` and the file with path `file` are the same.

        Problem: a symlink to the file and the file itself are NOT the same using 
        this.

        Args:
            file (FilePath): path to the file to check

        Raises:
            FileCompareException: if something goes wrong

        Returns:
            bool:   `True`, if the file is the same 
                    `False` else
        """
        try:
            tmp_path = os.path.abspath(file)

            tmp_path_obj = pathlib.Path(tmp_path)

            if not tmp_path_obj.is_file():
                raise FileCompareException(
                    "file \"{path}\" does not exist or is not a file!".format(path=tmp_path))

            tmp_size = tmp_path_obj.stat().st_size

            if self.size != tmp_size:
                return False

            tmp_hash = hashFile(tmp_path)

            if self.hash != tmp_hash:
                return False

        except Exception as excp:
            raise FileCompareException(excp)

        return True

################################################################################
def areHashesSame(file1: FilePath, file2: FilePath) -> bool:
    """Compares the BLAKE2 hashes of the given files.

    Returns `True` if the contents of both files are the same (have the same hash).

    Args:
        file1 (FilePath): first file to compare
        file2 (FilePath): second file to compare

    Raises:
        FileCompareException: if something goes wrong

    Returns:
        bool: `True`, if both files' content have the same BLAKE2 hash value.
              `False` else
    """
    try:
        hash1 = hashFile(file1)
        hash2 = hashFile(file2)

        if hash1 == hash2:
            return True
        else:
            return False
    except Exception as excp:
        raise FileCompareException(excp)

################################################################################
def hashFile(file: FilePath) -> str:
    """Generates a BLAKE2 hash of the file with the given path.

    Returns the hash as a hex string.
    If something goes wrong, it returns an `FileCompareException` instance.

    Raises:
            FileCompareException: if something goes wrong

    Args:
        file (FilePath): the file to return the BLAKE2 hash of

    Returns:
        str: the hex hash of the file's contend
    """
    ret_val = ""
    try:
        hash_func = hashlib.blake2b()

        file_data = pathlib.Path(file).read_bytes()

        hash_func.update(file_data)

        ret_val = hash_func.hexdigest()
    except Exception as excp:
        raise FileCompareException(excp)

    return ret_val
