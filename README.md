# Buildnis

![MIT license badge](https://img.shields.io/github/license/Release-Candidate/Buildnis)
![Python version badge](https://img.shields.io/github/pipenv/locked/python-version/Release-Candidate/Buildnis)
![PIP version badge](https://img.shields.io/pypi/v/buildnis)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Distributed, platform independent build system that can handle C++20 and Fortran modules and is flexible enough to build any language and handle (almost ;) any build step imaginable.

## Installation and Usage

## Contributing to the Project

See file [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

### configure_scripts

* if `env_script` is empty, `install_path` is used, if that is empty too, it is supposed that the executable is in the PATH.
* every script gets the architecture as a command line argument, like `x86` or `x64`. If they aren't needed, they can be ignored by the script.

## License

Buildnis is licensed under the MIT license, see file [LICENSE](./LICENSE).
