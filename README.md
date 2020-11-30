# robotframework-jupyterlibrary

> A [Robot Framework][] library for automating (testing of) [Jupyter][] end-user
> applications and extensions

[robot framework]: http://robotframework.org
[jupyter]: https://jupyter.org

|          pip          | conda |          docs           |            demo             |             pipes             |
| :-------------------: | :---: | :---------------------: | :-------------------------: | :---------------------------: |
| [![pip-badge][]][pip] | TODO  | [![docs-badge][]][docs] | [![binder-badge][]][binder] | [![worfklow-badge]][workflow] |

# Using

Write `.robot` files that use `JupyterLibrary` keywords.

```robotframework
*** Settings ***
Library           JupyterLibrary
Suite Setup       Wait for New Jupyter Server to be Ready
Test Teardown     Reset JupyterLab and Close
Suite Teardown    Terminate All Jupyter Servers

*** Test Cases ***
A Notebook in JupyterLab
    Open JupyterLab
    Launch a new JupyterLab Document
    Add and Run JupyterLab Code Cell
    Wait Until JupyterLab Kernel Is Idle
    Capture Page Screenshot
```

See the [acceptance tests][] for examples.

# Installation

```bash
pip install robotframework-jupyterlibrary
```

Or

```bash
conda install -c conda-forge robotframework-jupyterlibrary
```

## Development Installation

- get Firefox
  - Chrome works, too, but more fickle
- get [Miniconda3][] (as in Python 3.6+)
- clone this repo...

      git clone https://github.com/robots-from-jupyter/robotframework-jupyterlibrary
      cd robotframework-jupyterlibrary

- update and activate...

      conda env update
      conda activate robotframework-jupyterlibrary

- then...

      pip install -e . --no-deps --ignore-installed

- run the tests...

      python -m scripts.atest

# Free Software

JupyterLibrary is Free Software under the BSD-3-Clause License. It contains code
from a number of other projects:

- [Jyve][] ([BSD-3-Clause][jyve-license])
  - Initial implementations of robot keywords

[acceptance tests]:
  https://github.com/robots-from-jupyter/robotframework-jupyterlab
[miniconda3]: https://conda.io/miniconda.html
[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]:
  https://mybinder.org/v2/gh/robots-from-jupyter/robotframework-jupyterlibrary/master?urlpath=lab/tree/README.md
[workflow-badge]:
  https://github.com/bollwyvl/robotframework-jupyterlibrary/workflows/CI/badge.svg
[workflow]:
  https://github.com/bollwyvl/robotframework-jupyterlibrary/actions?query=branch%3Amaster+workflow%3ACI
[docs-badge]:
  https://readthedocs.org/projects/robotframework-jupyterlibrary/badge/?version=latest
[pip-badge]: https://img.shields.io/pypi/v/robotframework-jupyterlibrary.svg
[pip]: https://pypi.org/project/robotframework-jupyterlibrary
[docs]: https://robotframework-jupyterlibrary.readthedocs.io
[seleniumlibrary]: https://github.com/robotframework/SeleniumLibrary
[selibrary-license]:
  https://github.com/robotframework/SeleniumLibrary/blob/master/LICENSE.txt
[jyve]: https://github.com/deathbeds/jyve
[jyve-license]: https://github.com/deathbeds/jyve/blob/master/LICENSE
