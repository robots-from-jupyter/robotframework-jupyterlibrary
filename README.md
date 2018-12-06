# robotframework-jupyterlibrary
> A Robot Framework library for testing Jupyter end-user applications and extensions

[![binder-badge][]][binder] [![pipeline-badge]][pipeline]

> _TODO: rtd, pip, conda_

# Installation

## Development Installation
- get Firefox
- get Miniconda
- update and activate
```bash
conda env update
conda activate robotframework-jupyterlibrary
```
- then
```bash
pip install -e . --no-deps --ignore-installed
```
- run the tests
```
python -m scripts.atest
```

# Using
> _TODO: Figure out a documentation strategy that works with
         janky-imported resources_

Write `.robot` files that use `JupyterLibrary` keywords. See the
[acceptance tests](./atest/acceptance) for examples.


[binder-badge]: https://mybinder.org/badge_logo.svg
[binder]: https://mybinder.org/v2/gh/bollwyvl/robotframework-jupyterlibrary/ci/azure-pipelines?urlpath=lab
[pipeline-badge]: https://dev.azure.com/nickbollweg/nickbollweg/_apis/build/status/bollwyvl.robotframework-jupyterlibrary
[pipeline]: https://dev.azure.com/nickbollweg/nickbollweg/_build/latest?definitionId=2
