# Contributing to JupyterLibrary

## Get `CONDA_EXE`

- Get [Mambaforge](https://conda-forge.org/miniforge/)

```bash
mamba install -c conda-forge doit
# optional meta-dependency
mamba install -c conda-forge conda-lock
```

## Get the code

```bash
git clone http://github.com/robots-from-jupyter/robotframework-jupyterlibrary
cd robotframework-jupyterlibrary
```

## Doit

### Listing all the tasks

```shell
doit list
```

### Just run (just about) everything

```shell
doit release
```

### Lock Files

> After adding/changing any dependencies in `.github/env_specs`, the _lockfiles_ need to
> be refreshed in `.github/locks` and committed.

```shell
doit lock
```

> Bootstrapping from _no_ lockfiles requires an external provider of `conda-lock`. It
> may require running `doit lock` a few times to get a stable set of environment
> solutions.

### Reproducing CI failures

By default, the `doit` scripts use the lockfile most like where you are developing,
hoping for a better cache hit rate. On the same _operating system_, however, any of the
pre-solved lockfiles can be used, by specifying the `RJFL_LOCKFILE` environment
variable.

For example, if `linux-64` running `python3.8` with `jupyterlab 3` failed:

```bash
!/usr/bin/env bash
set -eux
RFJL_LOCKDIR=test/linux-64/py3.8/lab3 doit release
```

Or, in a `bat` script:

```bat
@echo on
set RFJL_LOCKDIR=test/win-64/py3.8/lab3
doit release
```

This will recreate the `test` environment with the specified lockfile, and repeat all
the steps.

### Environment Variables

A number of environment variables control how some of the `doit` tasks function.

|           variable |      default      | note                                               |
| -----------------: | :---------------: | -------------------------------------------------- |
|       `ATEST_ARGS` |       `[]`        | a JSON array of tokens to pass to `pabot`          |
|    `ATEST_RETRIES` |        `0`        | number of times to re-run failing tests            |
|    `ATEST_ATTEMPT` |        `0`        | where to start in the retry order                  |
|          `BROWSER` | `headlessfirefox` | which browser to use (only tested with FF)         |
|        `CONDA_EXE` |      `mamba`      | a custom `conda`-compatible tool to use            |
|        `IN_BINDER` |        `0`        | skips a number of steps                            |
| `INSTALL_ARTIFACT` |        ``         | `pip install` a built artifact instead of editable |

## Releasing

- [ ] merge all outstanding PRs
- [ ] start a release issue with a checklist (maybe like this one)
- [ ] ensure `pyproject.toml#/project/version` has been increased appropriately
- [ ] ensure the `HISTORY.ipynb` is up-to-date
- [ ] validate on binder
- [ ] validate on ReadTheDocs
- [ ] wait for a successful build of `main`
- [ ] download the `dist` archive and unpack somewhere (maybe a fresh `dist`)
- [ ] create a new release through the GitHub UI
  - [ ] paste in the relevant `HISTORY` entries
  - [ ] upload the artifacts
- [ ] actually upload to pypi.org
  ```bash
  doit publish
  ```
- [ ] postmortem
  - [ ] handle `conda-forge` feedstock tasks
  - [ ] validate on binder via simplest-possible gists
  - [ ] activate the version on ReadTheDocs
  - [ ] bump `pyproject.toml#/project/version` to next development version
  - [ ] update release procedures
