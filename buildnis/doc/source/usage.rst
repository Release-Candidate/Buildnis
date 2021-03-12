Installation and Usage
======================

Prerequisites
-------------

You need Python, at least version 3.9, you can get the latest version at `python.org <https://www.python.org/downloads/>`_

Installation
------------

Using a Virtual Environment
...........................

I _highly_ recommend that you use a virtual environment like `Virtualenv <https://virtualenv.pypa.io/en/latest/>`_
or `Pipenv <https://pypi.org/project/pipenv/>`_ to check out Buildnis.

Virtualenv Setup
,,,,,,,,,,,,,,,,

First install the package ``virtualenv`` using ``pip``:

.. code-block:: bash

    python -m pip install virtualenv


then set up a directory to use as the path for your virtual Python environment:

.. code-block:: bash

    python -m virtualenv PATH_TO_YOUR_VENV

with ``PATH_TO_YOUR_VENV`` the directory, in which you want to install the virtual environment.
This should generate a script to source (on Linux, OS X and other unixish platforms) or execute (Windows).
So, call or source the script:

Windows:

.. code-block:: cmd

    PATH_TO_YOUR_VENV\Scripts\activate.bat

Unix:

.. code-block:: shell

    source PATH_TO_YOUR_VENV/bin/activate

If you now install the packages, they're installed in this virtual environment and can't
break your 'real' Python installation.

When you want to leave the virtual environment, call the script ``deactivate``. More
detailed documentation of Virtualenv you find at the `Virtualenv User Guide <https://virtualenv.pypa.io/en/stable/user_guide.html>`_.

Pipenv Setup
,,,,,,,,,,,,


Installation of Buildnis
........................

You can install Buildnis using pip (also in a virtualenv, see `Virtualenv Setup`_) or pipenv (see `Pipenv Setup`_).

Installation using Pip
,,,,,,,,,,,,,,,,,,,,,,

.. code-block:: shell

    python -m pip install buildnis

To upgrade your installed version use

.. code-block:: shell

    python -m pip install --upgrade buildnis

Installation using Pipenv
,,,,,,,,,,,,,,,,,,,,,,,,,

.. code-block:: shell

    pipenv install buildnis

To upgrade your installed version use

.. code-block:: shell

    pipenv install --upgrade buildnis

Usage
-----

The best way to test Buildnis is to check out the test project from Github:
`Test Project on Github <https://github.com/Release-Candidate/Buildnis/tree/main/test_project>`_
and run Buildnis there:

.. code-block:: shell

    python -m buildnis --generated-conf-dir conf_out test_project/project_config.json

This reads the project's configuration ``test_project/project_config.json`` and stores all
generated configurations to the directory ``conf_out``.

If you want to delete the generated configuration files, call the program with the option ``--distclean``:

.. code-block:: shell

    python -m buildnis --distclean

To get an overview of all supported command-line options and arguments call Buildnis with
the argument ``-h`` or ``--help``:

.. code-block:: shell

    python -m buildnis --help

