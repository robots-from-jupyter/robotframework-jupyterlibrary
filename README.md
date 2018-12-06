# robotframework-jupyterlibrary
> A Robot Framework library for testing Jupyter end-user applications and extensions

---

> _TODO: binder, tests, pip, conda_

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
