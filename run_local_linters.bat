:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_local_linters.bat
:: Date:     15.Mar.2021
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Runs the local linters
black buildnis
pyflakes buildnis
pycodestyle buildnis
pydocstyle buildnis
flake8 buildnis
bandit -r buildnis
