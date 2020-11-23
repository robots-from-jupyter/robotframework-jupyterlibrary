# Contributing to JupyterLibrary

## [Environment](#Environment)

Get `$CONDA_EXE`:

- [miniforge](https://github.com/conda-forge/miniforge)
  - maybe get [mamba](https://github.com/mamba-org/mamba)

Use one of the CI environments:

- On Linux:

  ```bash
  $CONDA_EXE create -n --file locks/linux-64/py3.8/lab2/conda.lock
  ```

- On MacOs:

  ```zsh
  # or MacOS...
  $CONDA_EXE create -n --file locks/osx-64/py3.8/lab2/conda.lock
  ```

- On Windows:

  ```bat
  REM ...or Windows
  %CONDA_EXE% create -n --file locks/osx-64/py3.8/lab2/conda.lock
  ```

- activate it

## [Update Locks](#update-locks)

|  in | `env_specs/*.yml` |
| --: | ----------------- |
| out | `locks/*.lock`    |

```shell
python -m _scripts.lock
```

## [Build](#Build)

```shell
python setup.py sdist bdist_wheel
```

|  in | `src/**/*.py`         | `setup.{cfg,py}` |
| --: | --------------------- | ---------------- |
| out | `dist/*.{tar.gz,whl}` |

## [Unit Tests](#Unit-Tests)

```shell
pytest
```

## [Acceptance Tests](#Acceptance-Tests)

```shell
robot atest
```

## [Docs](#Docs)

```shell
sphinx-build -M html docs
```

## [Release](#Release)

```shell
twine upload dist/*.tar.gz dist/*.whl
```
