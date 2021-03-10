:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     test_install.bat
:: Date:     07.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Installs or upgrades the buildnis package using pip.
:: Uses pipenv, you can install that by `python -m pip install pipenv` and
:: installing the needed packages from the Buildnis root dir `Buildnis` - where
:: the `Pipfile` is located.
:: `pipenv install --dev` installs all needed dependencies to develop.

@echo off

:: pipenv run pip install --upgrade -i https://test.pypi.org/simple/ example-pkg-Release-Candidate-example_pkg_Release_Candidate_Username
pipenv run pip install --upgrade buildnis
