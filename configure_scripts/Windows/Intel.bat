:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     Intel.bat
:: Date:     15.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: searches for the Intel compilers setting batch file.

@echo off

:: ONEAPI_ROOT
:: C:\Program Files (x86)\Intel\oneAPI\

:: Intel needs intel64 or ia32 as arguments to set 64 or 32 bit compilers
set X64_ARGUMENT=intel64
set I86_ARGUMENT=ia32

:: parse command line arguments
:PARSE_ARGS
if /i "%1"==""    goto :END_PARSE_ARGS
if /i "%1"=="x64" (set CMD_ARG=%X64_ARGUMENT%) & shift & goto :PARSE_ARGS
if /i "%1"=="x86" (set CMD_ARG=%I86_ARGUMENT%) & shift & goto :PARSE_ARGS
:END_PARSE_ARGS

set ICL_VERSION=
set ICX_VERSION=
set IFORT_VERSION=
set IFX_VERSION=
set PYTHON_VERSION=

:: search for the environment script setvars.bat
if exist "%ONEAPI_ROOT%setvars.bat" (
    set ENV_SCRIPT="%ONEAPI_ROOT%setvars.bat"
   
) else if exist "%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat" (
    set ENV_SCRIPT="%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat"
   
)

if /i "%ICL_VERSION%"=="" set ICL_VERSION=""
if /i "%ICX_VERSION%"=="" set ICX_VERSION=""
if /i "%IFORT_VERSION%"=="" set IFORT_VERSION=""
if /i "%IFX_VERSION%"=="" set IFX_VERSION=""
if /i "%PYTHON_VERSION%"=="" set PYTHON_VERSION=""

:: JSON output
echo {
echo "build_tools": 
echo [
echo     {
echo         "name": "Intel C++ Classic",
echo         "name_long": %ICL_VERSION%,
echo         "version": "",
echo         "build_tool_exe": "icl",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel DPC++/C++",
echo         "name_long": %ICX_VERSION%,
echo         "version": "",
echo         "build_tool_exe": "icx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Fortran Classic",
echo         "name_long": %IFORT_VERSION%,
echo         "version": "",
echo         "build_tool_exe": "ifort",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Fortran (ifx)",
echo         "name_long": %IFX_VERSION%,
echo         "version": "",
echo         "build_tool_exe": "ifx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Python",
echo         "name_long": %PYTHON_VERSION%,
echo         "version": "",
echo         "build_tool_exe": "python",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     }
echo ]
echo }



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

