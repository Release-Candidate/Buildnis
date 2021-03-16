:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_local_linters.bat
:: Date:     15.Mar.2021
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Runs the local linters
black buildnis test_project
pyflakes buildnis test_project
pycodestyle buildnis test_project
pydocstyle buildnis test_project
flake8 buildnis test_project
isort buildnis test_project
bandit -r buildnis test_project
