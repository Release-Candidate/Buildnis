:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     make_package.bat
:: Date:     06.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: generates a Python PIP package in the current working directory and uploads
:: it to Pypi.

@echo off

rmdir /S /Q build 
rmdir /S /Q dist
rmdir /S  /Q example_pkg_Release_Candidate_Username.egg-info

python -m build

twine upload --repository testpypi dist/* --config-file %APPDATA%\pip\pip.ini

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
