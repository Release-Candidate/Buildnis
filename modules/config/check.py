# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     check.py
# Date:     16.Feb.2021
###############################################################################

from modules.config import Arch, OSName


class Check:
    """Checks if all build tools are present.
    
    Runs all build tool scripts in `configure_scripts`.

    Attributes:
    
    Methods:
    
    """
    ###########################################################################
    def __init__(self, os: OSName, arch: Arch) -> None:
        """Constructor of Check, runs all build tool scripts in 
        `configure_scripts`.

        All build tool scripts in the `os` subdirectory of `configure_scripts` 
        are run, the CPU architecture `arch` is passed as an argument to each
        script.

        Args:
            os (OSName): [description]
            arch (Arch): [description]
        """
        pass


    
