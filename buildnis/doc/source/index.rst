Welcome to Buildnis' documentation!
====================================

Buildnis is a distributed, platform independent build system that can handle C++20 and
Fortran modules and is flexible enough to build any language and handle (almost ;)
any build step imaginable. It is written in Python and needs a Python interpreter, at
least version 3.9.

The main goal is to have a build system with only the minimum needed configuration and specially
user interaction to build software on all supported OSes (Linux, Mac OS X and Windows - alphabetically).
The list of currently automatically supported compilers and build tools can be found at the chapter :ref:`supported_configs`.
How to customize Buildnis for your needs can be found at :ref:`customizing_buildnis`,
how to extend it, that means adding other OSes or CPU architectures or stuff that need changes in the Python code of
Buildnis itself, can be found in the chapter :ref:`extending_buildnis`.


.. toctree::
   :hidden:
   :caption: Links

   GitHub Project Page <https://github.com/Release-Candidate/Buildnis>
   PyPI (pip) Package <https://pypi.org/project/buildnis/>
   Documentation at Read the Docs <https://buildnis.readthedocs.io/>
   Report a Bug or a Feature Request <https://github.com/Release-Candidate/Buildnis/issues/new/choose>
   Issue Tracker at GitHub <https://github.com/Release-Candidate/Buildnis/issues>

To get you started, short how-tos to get Buildnis up and running:

.. toctree::
   :maxdepth: 5
   :caption: Installation and Usage

   usage
   commandline
   configuration
   stages
   license

.. toctree::
   :hidden:
   :maxdepth: 5
   :caption: Customizing

   supported_configs
   customizing
   extending

.. toctree::
   :hidden:
   :maxdepth: 5
   :caption: Developing Buildnis

   dev_index

.. toctree::
   :hidden:
   :maxdepth: 5
   :caption: Indices

   genindex
   py-modindex
