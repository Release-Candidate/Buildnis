:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     test_install.bat
:: Date:     07.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@echo off

call env_to_test\Scripts\activate.bat

:: python -m pip install --upgrade -i https://test.pypi.org/simple/ example-pkg-Release-Candidate-example_pkg_Release_Candidate_Username
python -m pip install --upgrade buildnis

GOTO :EOF


:: trim spaces off the strings
:TRIM
SetLocal EnableDelayedExpansion
Call :TRIMHELPER %%%1%%
EndLocal & set %1=%helper_tmp%
GOTO :EOF

:TRIMHELPER
set helper_tmp=%*
GOTO :EOF
