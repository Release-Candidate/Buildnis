:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_local_linters.bat
:: Date:     15.Mar.2021
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Runs the local linters
black buildnis test_project tests
pyflakes buildnis test_project tests
pycodestyle buildnis test_project tests
pydocstyle buildnis test_project tests
flake8 buildnis test_project tests
isort buildnis test_project tests
bandit -r buildnis test_project tests
