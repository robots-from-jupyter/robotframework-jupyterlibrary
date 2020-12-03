## Contributing to JupyterLibrary

### Get `CONDA_EXE`

- Get [miniforge](https://github.com/conda-forge/miniforge)

```bash
conda install -c conda-forge doit
# optional meta-dependencies
conda install -c conda-forge conda-lock mamba
```

### Get the code

```bash
git clone http://github.com/robots-from-jupyter/robotframework-jupyterlibrary
cd robotframework-jupyterlibrary
```

### Doit

#### Listing all the tasks

```shell
doit list
```

#### Just run (just about) everything

```shell
doit release
```

#### Lock Files

> After adding/changing any dependencies in `.github/env_specs`, the _lockfiles_
> need to be refreshed in `.github/locks` and committed.

```shell
doit lock
```

> Bootstrapping from _no_ lockfiles requires an external provider of
> `conda-lock`. It may require running `doit lock` a few times to get a stable
> set of environment solutions.

#### Reproducing CI failures

By default, the `doit` scripts use the lockfile most like where you are
developing, hoping for a better cache hit rate. On the same _operating system_,
however, any of the pre-solved lockfiles can be used, by specifying the
`RJFL_LOCKFILE` environment variable.

For example, if `linux-64` running `python3.6` with `jupyterlab 1` failed:

```bash
#!/usr/bin/env bash
set -eux
RFJL_LOCKDIR=test/linux-64/py3.6/lab1 doit release
```

Or, in a `bat` script:

```bat
@echo on
set RFJL_LOCKDIR=test/win-64/py3.9/lab1
doit release
```

This will recreate the `test` environment with the specified lockfile, and
repeat all the steps.
