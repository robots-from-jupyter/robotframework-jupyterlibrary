---
name: Release
about: Prepare for a release
labels: maintenance
---

- [ ] merge all outstanding PRs
  - [ ] #PR ...
- [ ] ensure the versions have been bumped (check with `doit`)
- [ ] ensure `HISTORY.ipynb` is up-to-date
  - [ ] move the new release to the top of the stack
- [ ] validate on binder
- [ ] validate on ReadTheDocs
- [ ] wait for a successful build of `main`
- [ ] download the `dist` archive and unpack somewhere (maybe a fresh `dist`)
- [ ] create a new release through the GitHub UI
  - [ ] paste in the relevant `HISTORY.ipynb` entries
  - [ ] upload the artifacts
- [ ] actually upload to pypi.org
  ```bash
  cd dist
  twine upload *.tar.gz *.whl
  ```
  - [ ] PyPI URL
- [ ] postmortem
  - [ ] handle `conda-forge` feedstock tasks
    - [ ] https://github.com/conda-forge/robotframework-jupyterlibrary-feedstock/pull/PULL
    - [ ] https://anaconda.org/conda-forge/robotframework-jupyterlibrary/files?version=VERSION
  - [ ] validate on binder via simplest-possible gists
  - [ ] bump to next development version
  - [ ] rebuild locks
    - [ ] `.github/locks`
    - [ ] `yarn.lock`
  - [ ] handle linter opinion changes
  - [ ] update `HISTORY.ipynb`
  - [ ] update release procedures with lessons learned
