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

:: search for the environment script setvars.bat
if exist "%ONEAPI_ROOT%setvars.bat" (
    set ENV_SCRIPT="%ONEAPI_ROOT%setvars.bat"
    echo %ENV_SCRIPT%
) else if exist "%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat" (
    set ENV_SCRIPT="%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat"
    echo %ENV_SCRIPT%
)


:: JSON output
echo {
echo "build_tools": 
echo [
echo     {
echo         "name": "Intel C++ Classic",
echo         "name_long": "",
echo         "version": "",
echo         "build_tool_exe": "icl",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel DPC++/C++",
echo         "name_long": "",
echo         "version": "",
echo         "build_tool_exe": "icx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Fortran Classic",
echo         "name_long": "",
echo         "version": "",
echo         "build_tool_exe": "ifort",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Fortran (ifx)",
echo         "name_long": "",
echo         "version": "",
echo         "build_tool_exe": "ifx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     },
echo     {
echo         "name": "Intel Python",
echo         "name_long": "",
echo         "version": "",
echo         "build_tool_exe": "python",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
echo     }
echo ]
echo }