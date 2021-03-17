:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     run_test.bat
:: Date:     16.Mar.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::pytest --hypothesis-show-statistics --cov=./ --cov-report=xml
:: pytest --hypothesis-show-statistics --no-cov --show-capture=no

pytest --hypothesis-show-statistics --no-cov -n 12
