# robotframework-jupyterlibrary
> A [Robot Framework][] library for automating (testing of) [Jupyter][] end-user applications and extensions

[Robot Framework]: http://robotframework.org
[Jupyter]: https://jupyter.org

| docs                    | demo                        | pipes                         |
|:-----------------------:|:---------------------------:|:-----------------------------:|
| [![docs-badge][]][docs] | [![binder-badge][]][binder] | [![pipeline-badge]][pipeline] |


# Using
Write `.robot` files that use `JupyterLibrary` keywords.

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

See the [acceptance tests][] for examples.


# Installation
> _TODO: release on pypi, conda-forge_

## Development Installation

- get Firefox
  - Chrome works, too, but more fickle
- get [Miniconda3][] (as in Python 3.6+)
- clone this repo...

      git clone https://github.com/bollwyvl/robotframework-jupyterlibrary
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

- [SeleniumLibrary][] ([APL-2.0][selibrary-license])
  - backport of `Press Keys`
- [Jyve][] ([BSD-3-Clause][jyve-license])
  - Initial implementations of robot keywords

[acceptance tests]: https://github.com/bollwyvl/robotframework-jupyterlab
[Miniconda3]: https://conda.io/miniconda.html
[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]: https://mybinder.org/v2/gh/bollwyvl/robotframework-jupyterlibrary/master?urlpath=lab/tree/README.md
[pipeline-badge]: https://dev.azure.com/nickbollweg/nickbollweg/_apis/build/status/bollwyvl.robotframework-jupyterlibrary
[pipeline]: https://dev.azure.com/nickbollweg/nickbollweg/_build/latest?definitionId=2
[docs-badge]: https://readthedocs.org/projects/robotframework-jupyterlibrary/badge/?version=latest
[docs]: https://robotframework-jupyterlibrary.readthedocs.io

[SeleniumLibrary]: https://github.com/robotframework/SeleniumLibrary
[selibrary-license]: https://github.com/robotframework/SeleniumLibrary/blob/master/LICENSE.txt

[Jyve]: https://github.com/deathbeds/jyve
[jyve-license]: https://github.com/deathbeds/jyve/blob/master/LICENSE
