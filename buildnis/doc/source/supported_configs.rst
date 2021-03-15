.. _supported_configs:

Supported Configurations
========================

Supported means that Buildnis can automatically find these executables, if they're installed
in a default location or in a directory that is in the PATH.

If the compiler or tool needed for your build isn't in this list, you have to customize and add
some scripts in Buildnis or your project, see :ref:`customizing_buildnis`.

If your OS or CPU architecture isn't supported, you have to change Buildnis itself, but
that's not much work to do in the Python source code, see :ref:`extending_buildnis`.

Supported OSes
--------------

In alphabetical order:

* Linux (tested with Fedora Rawhide, RedHat, Suse Tumbleweed and Ubuntu)
* Mac OS X (tested with Bug Sur)
* Windows (tested using Windows 10)

Supported C++ Compilers
-----------------------

All compilers in this list are either free (open source) or free as in free beer for at
open source projects or non-commercial use. See the linked websites for details!

Linux
.....

* GCC - the default compiler for Linux. `<https://gcc.gnu.org/>`_
* Clang `<https://clang.llvm.org/>`_
* AMD AOCC - uses LLVM `<https://developer.amd.com/amd-aocc/>`_
* Nvidia HPC Compilers - ex Portland compilers `<https://developer.nvidia.com/hpc-compilers>`_
* Intel OneAPI C++ and DPC++ `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit.html>`_

Mac OS X
........

* Clang - the default compiler for OS X, part of XCode package `<https://developer.apple.com/xcode/>`_
* Intel OneAPI C++ and DPC++ Intel CPU only `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit.html>`_

Windows
.......

* MS Visual Studio cl - the default compiler for Windows `<https://visualstudio.microsoft.com/vs/>`_
* Clang included in Visual Studio `<https://visualstudio.microsoft.com/vs/>`_
* Intel oneAPI C++ and DPC++ `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit.html>`_

Supported Fortran Compilers
---------------------------

All compilers in this list are either free (open source) or free as in free beer for at
open source projects or non-commercial use. See the linked websites for details!

Linux
.....

* GFortran (GCC) - default Fortran compiler for Linux `<https://gcc.gnu.org/wiki/GFortran>`_
* FLang (LLVM) - Fedora Rawhide has it in its repository `<https://releases.llvm.org/11.0.0/tools/flang/docs/ReleaseNotes.html>`_
* AMD AOCC - it's called 'optimizing C and C++, but includes a Fortran compiler, FLang' `<https://developer.amd.com/amd-aocc/>`_
* Nvidia HPC Compilers - ex Portland compilers `<https://developer.nvidia.com/hpc-compilers>`_
* Intel OneAPI IFort Fortran Classic and IFX, Fortran is included in the HPC kit `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/hpc-toolkit.html>`_

Mac OS X
........

* Intel OneAPI IFort Fortran Classic and IFX, Fortran is included in the HPC kit `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/hpc-toolkit.html>`_

Windows
.......

* Intel oneAPI IFort Fortran Classic and IFX , Fortran is included in the HPC kit `<https://software.intel.com/content/www/us/en/develop/tools/oneapi/hpc-toolkit.html>`_

Supported Interpreters
----------------------

Linux
.....

* Python `<https://www.python.org/downloads/>`_
* Java  `<https://jdk.java.net/15/>`_

Mac OS X
........

* Python `<https://www.python.org/downloads/>`_
* Java `<https://jdk.java.net/15/>`_

Windows
.......

* Python `<https://www.python.org/downloads/>`_
* Java `<https://jdk.java.net/15/>`_

Supported Documentation Tools
-----------------------------

Linux
.....

* Doxygen `<https://www.doxygen.nl/download.html>`_
* Sphinx - install using ``pip`` `<https://www.sphinx-doc.org/en/master/>`_

Mac OS X
.........

* Doxygen `<https://www.doxygen.nl/download.html>`_
* Sphinx - install using ``pip`` `<https://www.sphinx-doc.org/en/master/>`_

Windows
.......

* Doxygen `<https://www.doxygen.nl/download.html>`_
* Sphinx - install using ``pip`` `<https://www.sphinx-doc.org/en/master/>`_

Supported Build Tools
---------------------

Anything that doesn't fit the other categories.
