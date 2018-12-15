# robotframework-jupyterlibrary
> A [Robot Framework][] library for automating (testing of) [Jupyter][] end-user applications and extensions

[Robot Framework]: http://robotframework.org
[Jupyter]: https://jupyter.org

[![binder-badge][]][binder] [![pipeline-badge]][pipeline]

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

[acceptance tests]: https://github.com/bollwyvl/robotframework-jupyterlab
[Miniconda3]: https://conda.io/miniconda.html
[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]: https://mybinder.org/v2/gh/bollwyvl/robotframework-jupyterlibrary/master?urlpath=lab/tree/README.md
[pipeline-badge]: https://dev.azure.com/nickbollweg/nickbollweg/_apis/build/status/bollwyvl.robotframework-jupyterlibrary
[pipeline]: https://dev.azure.com/nickbollweg/nickbollweg/_build/latest?definitionId=2
