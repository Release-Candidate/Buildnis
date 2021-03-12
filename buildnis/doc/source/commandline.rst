Command Line Arguments
======================

Normally (depending on the project's configuration) you do not need to use any argument or
target to configure and build software using Buildnis, it does run everything that is needed
to be able to build the default targets, but never the ``--install`` - which would install
the generated files - or ``--clean``/``--distclean`` stages, which would delete the generated files.

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

.. note::

    ``-v`` adds verbosity, it is not short for ``--version``!

.. code-block:: shell

    python -m buildnis --version

prints

.. code-block:: text

    Buildnis 0.2.6

Main Argument - The Project Configuration
-----------------------------------------

