:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_local_linters.bat
:: Date:     15.Mar.2021
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Runs the local linters
black buildnis tests
pyflakes buildnis tests
pycodestyle buildnis tests
pydocstyle buildnis tests
flake8 buildnis tests
isort buildnis tests
bandit -r buildnis tests
