:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_test.bat
:: Date:     16.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::pytest --hypothesis-show-statistics --cov=./ --cov-report=xml
:: pytest --hypothesis-show-statistics --no-cov --show-capture=no

:: to get a list of tests ...
pytest --collect-only

:: do not run tests that run the whole program in parallel, the configuration files will
:: be deleted when a instance is still runnig.
pytest --hypothesis-show-statistics --no-cov -m "not run_program" -n 12 %1
::pytest --hypothesis-show-statistics --no-cov -m "run_program" %1
