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
    E.g. instead of ``--dist-clean`` you could also write ``--di``

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

# ``--configure``

--configure           Configure the project.
  --build [TARGET ...]  Build the project. If a list of targets is given, these targets are build. The default is to build the default target.
  --install [TARGET ...]
                        Install the given targets. If no target is given, installs the project's default target.
  --clean               Clean the project. Deletes all files and directories generated during the build.
  --distclean           Start from scratch, delete generated configuration. Deletes all files and directories generated during the build and the configuration.

Logging Options
---------------

--log-file LOG_FILE   If this is set, the program writes verbose messages to LOG_FILE, does not change output to the console. Default is none.
  -q, --quiet           Run quiet, only output error messages.
  -v, --verbose         Increase verbosity of the program, get more messages. Can be used more than once, like "-vv"
  --debug               Set logging level to the highest available, the same as "-vv"


