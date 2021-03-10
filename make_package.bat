:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     make_package.bat
:: Date:     06.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: generates a Python PIP package in the current working directory and uploads
:: it to Pypi.
:: Uses pipenv, you can install that by `python -m pip install pipenv` and
:: installing the needed packages from the Buildnis root dir `Buildnis` - where
:: the `Pipfile` is located.
:: `pipenv install --dev` installs all needed dependencies to develop.

@echo off

rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q example_pkg_Release_Candidate_Username.egg-info
rmdir /S /Q buildnis.egg-info

pipenv run python -m build


:: pipenv run twine upload --repository testpypi dist/* --config-file %APPDATA%\pip\pip.ini

pipenv run twine upload --repository pypi dist/* --config-file %APPDATA%\pip\pip.ini
