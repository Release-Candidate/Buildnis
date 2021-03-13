Command Line Arguments
======================

Normally (depending on the project's configuration) you do not need to use any argument or
target to configure and build software using Buildnis, it does run everything that is needed
to be able to build the default targets, but never the ``--install`` - which would install
the generated files - or ``--clean``/``--distclean`` stages, which would delete the generated files.

So with a default project JSON configuration named ``project_config.json`` in the current
working directory, you only need to call Buildnis like this:

.. code-block:: shell

    python -m buildnis

After the build finishes successfully, you can install the generated files using the ``--install``
argument.

.. code-block:: shell

    python -m buildnis --install

Depending where the project is configured to install the files to, you need to run this
as user root or as administrator.

For unixish OSes (that use ``sudo``):

.. code-block:: shell

    sudo python -m buildnis --install

For any other OS you have to start a shell (command interpreter) as an administrator, and
install from that shell:

.. code-block:: shell

    python -m buildnis --install

.. note::

    With long arguments you only need to input that part of the argument, that makes it unique.
    E.g. instead of ``--distclean`` you could also write ``--di``

Show Help Text
--------------

The arguments ``-h`` or ``--help`` shows the help text.

.. code-block:: shell

    python -m buildnis --help

Show Version
------------

The argument ``--version`` shows the help text.

.. code-block:: shell

    python -m buildnis --version

prints

.. code-block:: text

    Buildnis 0.2.6

.. note::

    ``-v`` adds verbosity, it is not short for ``--version``!

Main Argument - The Project Configuration
-----------------------------------------

The main argument of the command line is the path to the project configuration JSON file.
If none is given, the default of ``project_config.json`` in the current directory is used.

Example, to build the project with the main configuration file in the directory ``test_project``:

.. code-block:: shell

    python -m buildnis ./test_project/project_config.json

.. note::

    You can use normal slashes ``/`` for paths on Windows too, no need for windows-like
    backslashes (``\``) as path arguments to Python.



Build Stages
------------

* ``--configure``
* ``--build``
* ``--install``
* ``--clean``
* ``--distclean``

Example, to configure the project with the main configuration file in the directory ``test_project``:

.. code-block:: shell

    python -m buildnis --configure ./test_project/project_config.json

Example, to build the default targets of the with the main configuration file in the directory ``test_project``:

.. code-block:: shell

    python -m buildnis --build ./test_project/project_config.json

Example, to build the targets ``documentation`` and ``fortran_static`` of the project
with the main configuration file in the directory ``test_project``.

.. warning::

    You need to be careful
    to let the command line parser know the end of the target list. Either use a double dash ``--``
    or add the targets after the project config file.

.. code-block:: shell

    python -m buildnis --build documentation fortran_static -- ./test_project/project_config.json
    python -m buildnis ./test_project/project_config.json --build documentation fortran_static

.. note::

    You can use normal slashes ``/`` for paths on Windows too, no need for windows-like
    backslashes (``\``) as path arguments to Python.

Output and Script Paths
-----------------------

* ``--generated-conf-dir DIR_PATH``
* ``--conf-script-dir DIR_PATH``

Logging Options
---------------

* ``-q`` or ``--quiet``
* ``-v`` or ``--verbose``
* ``--debug`` or ``-vv`` or ``--verbose --verbose``
* ``--log-file LOG_FILE``
