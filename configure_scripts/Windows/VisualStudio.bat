:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     VisualStudio.bat
:: Date:     15.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Searches for Visual Studio 2017/2019 (and newer) installations, outputs the
:: gathered information JSON formatted.

@echo off

:: Commandline to call `vswhere` whith, the MS program to search for Visual
:: Studio installations and their properties.
set VS_WHERE="%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
set VS_WHERE_CMDLINE=%VS_WHERE% -prerelease


:: VS needs AMD64 or x86 as arguments to set 64 or 32 bit compilers
set X64_ARGUMENT=-arch=amd64
set I86_ARGUMENT=-arch=x86

:: parse command line arguments
:PARSE_ARGS
if /i "%1"==""    goto :END_PARSE_ARGS
if /i "%1"=="x64" (set CMD_ARG=%X64_ARGUMENT%) & shift & goto :PARSE_ARGS
if /i "%1"=="x86" (set CMD_ARG=%I86_ARGUMENT%) & shift & goto :PARSE_ARGS
:END_PARSE_ARGS

setlocal enabledelayedexpansion

:: get installation path
set /a IDX=0
for /f "delims=" %%l in ('%VS_WHERE_CMDLINE% -property installationPath') do (
    set RESULT[!IDX!].install_path=%%l
    call :TRIM RESULT[!IDX!].install_path
    set /a "IDX+=1"
)

:: get the 'short' name
set /a IDX=0
for /f "delims=" %%l in ('%VS_WHERE_CMDLINE% -property catalog_productName') do (
    set RESULT[!IDX!].name=%%l
    call :TRIM RESULT[!IDX!].name
    set /a "IDX+=1"
)

:: get the year part of VS' name
set /a IDX=0
for /f "delims=" %%l in ('%VS_WHERE_CMDLINE% -property catalog_productLineVersion') do (
    set RESULT[!IDX!].year=%%l
    call :TRIM RESULT[!IDX!].year
    set /a "IDX+=1"
)

:: full product name
set /a IDX=0
for /f "delims=" %%l in ('%VS_WHERE_CMDLINE% -property displayName') do (
    set RESULT[!IDX!].name_long=%%l
    call :TRIM RESULT[!IDX!].name_long
    set /a "IDX+=1"
)

:: version string
set /a IDX=0
for /f "delims=" %%l in ('%VS_WHERE_CMDLINE% -property catalog_productDisplayVersion') do (
    set RESULT[!IDX!].version=%%l
    call :TRIM RESULT[!IDX!].version
    set /a "IDX+=1"
)

:: check environment script, if it exists, add it
set /a LOOP_IDX=0
:LOOP1
if defined RESULT[!LOOP_IDX!].install_path (
    call set a=%%RESULT[!LOOP_IDX!].install_path%%\Common7\Tools\VsDevCmd.bat
    if exist "!a!" (
        set RESULT[!LOOP_IDX!].env_script=!a!
        call :TRIM RESULT[!LOOP_IDX!].env_script
    )
    set /a "LOOP_IDX+=1"
    goto :LOOP1
)

:: JSON output
echo {
echo "build_tools":
echo [
set /a LOOP_IDX=0
:LOOP
if defined RESULT[!LOOP_IDX!].install_path (
    echo     {
    call echo         "name": "%%RESULT[!LOOP_IDX!].name%% %%RESULT[!LOOP_IDX!].year%%",
    call echo         "name_long": "%%RESULT[!LOOP_IDX!].name_long%% %%RESULT[!LOOP_IDX!].version%%",
    call echo         "version": "",
    call echo         "build_tool_exe": "cl",
    call echo         "install_path": "",
    call echo         "env_script": "%%RESULT[!LOOP_IDX!].env_script:\=\\%%"
    set /a "LOOP_IDX+=1"
    if defined RESULT[!LOOP_IDX!].install_path (
        echo     },
    ) else (
        echo     }
    )
    goto :LOOP
)
echo ]
echo }

EndLocal
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