""" project paths, files and utilities, used by `dodo.py` and `_scripts/`
"""
from pathlib import Path

import platform
import os
import sys
import shutil
from configparser import ConfigParser

for _yaml in ["yaml", "ruamel_yaml", "ruamel.yaml"]:
    try:
        yaml = __import__(_yaml)
        if _yaml == "ruamel.yaml":
            yaml = yaml.yaml
        safe_load = yaml.safe_load
        safe_dump = yaml.safe_dump
        break
    except ImportError:
        pass

assert safe_load, "need at least a yaml parser"


CI = safe_load(os.environ.get("CI", "0"))
INSTALL_ARTIFACT = safe_load(os.environ.get("INSTALL_ARTIFACT", "0"))
IN_BINDER = safe_load(os.environ.get("IN_BINDER", "0"))
PLATFORM = platform.system()
BROWSER = os.environ.get("BROWSER", "headlessfirefox")
CAN_CONDA_LOCK = shutil.which("conda-lock") is not None

CONDA_EXE = os.environ.get("CONDA_EXE")

if CONDA_EXE is None and PLATFORM == "windows":
    CONDA_EXE = "conda.bat"

if CONDA_EXE is None:
    CONDA_EXE = "conda"

THIS_CONDA_SUBDIR = {
    "Linux": "linux-64",
    "Darwin": "osx-64",
    "Windows": "win-64",
}[PLATFORM]
THIS_PYTHON = "".join(map(str, sys.version_info[:2]))

THIS_LAB = None
try:
    from jupyterlab import __version__ as THIS_LAB
except:
    pass

if CI:
    print(f"{THIS_CONDA_SUBDIR}_py{THIS_PYTHON}_lab{THIS_LAB}")

# commands
PY = ["python"]
PYM = [*PY, "-m"]
SCRIPT_LOCK = [*PYM, "_scripts.lock"]


SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
DODO = ROOT / "dodo.py"


SRC = ROOT / "src" / "JupyterLibrary"
VERSION_FILE = SRC / "VERSION"
LICENSE = ROOT / "LICENSE"
VERSION = VERSION_FILE.read_text().strip()
PY_SRC = [*SRC.rglob("*.py")]
SETUP_CFG = ROOT / "setup.cfg"

_cfg_parser = ConfigParser()
_cfg_parser.read(SETUP_CFG)

SETUP = {k: dict(_cfg_parser[k]) for k in _cfg_parser.sections()}
SETUP_CRUFT = [
    ROOT / "setup.py",
    ROOT / "MANIFEST.in",
    SETUP_CFG,
    VERSION_FILE,
    LICENSE,
]
BINDER = ROOT / ".binder"
ATEST = ROOT / "atest"
ROBOT_SRC = [*SRC.rglob("*.resource")]

# things we build
BUILD = ROOT / "build"
BUILD.exists() or BUILD.mkdir()
ATEST_OUT = BUILD / "test/output"
ATEST_OUT_XML = "output.xml"

DIST = ROOT / "dist"
IMPORTABLE = "robotframework_jupyterlibrary"
SDIST = DIST / f"""{IMPORTABLE.replace("_", "-")}-{VERSION}.tar.gz"""
WHEEL = DIST / f"{IMPORTABLE}-{VERSION}-py3-none-any.whl"
HASH_DEPS = [SDIST, WHEEL]
SHA256SUMS = DIST / "SHA256SUMS"


# docs
DOCS = ROOT / "docs"
RTD_ENV = DOCS / "rtd.yml"
DOCS_CONF_PY = DOCS / "conf.py"
DOCS_BUILDINFO = BUILD / "docs/html/.buildinfo"

# demo
LABEXTXT = BINDER / "labex.txt"
LAB_EXTENSIONS = sorted(
    {
        ext.strip()
        for ext in LABEXTXT.read_text().strip().splitlines()
        if not ext.strip().startswith("#")
    }
)
APP_DIR = ROOT / "_lab"
APP_MODULES = APP_DIR / "labextensions"
ALL_APP_MODULES = [*APP_MODULES.glob("*.tgz")]

# fixed name, but contains a link to main.<hash>.js
APP_INDEX = APP_DIR / "static" / "index.html"

# partial environments
GITHUB = ROOT / ".github"
WORKFLOWS = GITHUB / "workflows"
LOCKS = GITHUB / "locks"
ENV_SPECS = GITHUB / "env_specs"
ENVS = ROOT / ".envs"

ENV_NAMES = ["test", "lint", "docs", "meta"]

CONDA_RUN = [CONDA_EXE, "run"]

if IN_BINDER:
    RUN_IN = {
        env: [*CONDA_RUN, "-p", os.environ["NB_PYTHON_PREFIX"]] for env in ENV_NAMES
    }
elif CI:
    RUN_IN = {env: [*CONDA_RUN, "-n", env] for env in ENV_NAMES}
else:
    RUN_IN = {
        env: [*CONDA_RUN, "--live-stream", "--no-capture-output", "-p", ENVS / env]
        for env in ENV_NAMES
    }

LOCK_NAME = "conda.lock"
CONDA_LISTS = {env: BUILD / env / LOCK_NAME for env in ENV_NAMES}
PIP_LISTS = {env: BUILD / env / "pip.freeze" for env in ENV_NAMES}

WORKFLOW_CI = WORKFLOWS / "ci.yml"
WORKFLOW_CI_YAML = safe_load(WORKFLOW_CI.read_text())
TEST_MATRIX = WORKFLOW_CI_YAML["jobs"]["test"]["strategy"]["matrix"]
PYTHONS = TEST_MATRIX["python-version"]
LABS = TEST_MATRIX["lab-version"]
PLATFORMS = TEST_MATRIX["conda-subdir"]

EXCLUDES = {
    (
        "test",
        ex.get("conda-subdir"),
        ex.get("python-version"),
        ex.get("lab-version"),
    ): True
    for ex in TEST_MATRIX.get("exclude", [])
}


def _is_excluded(flow, pf, py, lab):
    for flow_, pf_, py_, lab_ in EXCLUDES.keys():
        if flow_ is not None:
            if flow_ != flow:
                continue
        if pf_ is not None:
            if pf_ != pf:
                continue
        if py_ is not None:
            if py_ != py:
                continue
        if lab_ is not None:
            if lab_ != lab:
                continue
        return True
    return False


ENVENTURES = {
    ("test", pf, py, lab): LOCKS / "test" / pf / py / lab / LOCK_NAME
    for pf in PLATFORMS
    for lab in LABS
    for py in PYTHONS
    if not _is_excluded("test", pf, py, lab)
}

ENVENTURES.update(
    {("lint", pf, None, None): LOCKS / "lint" / pf / LOCK_NAME for pf in PLATFORMS}
)

ENVENTURES.update(
    {("docs", pf, None, None): LOCKS / "docs" / pf / LOCK_NAME for pf in PLATFORMS}
)

ENVENTURES.update(
    {("meta", pf, None, None): LOCKS / "meta" / pf / LOCK_NAME for pf in PLATFORMS}
)

THIS_META_ENV_LOCK = LOCKS / "meta" / THIS_CONDA_SUBDIR / LOCK_NAME
THIS_META_ENV_HISTORY = ENVS / "meta" / "conda-meta" / "history"

ENV_DEPS = {
    (flow, pf, py, lab): [
        *([ENV_SPECS / "_base.yml"] if flow not in ["meta"] else []),
        ENV_SPECS / f"{flow}.yml",
        *(
            [ENV_SPECS / f"{flow}-{py}.yml"]
            if (ENV_SPECS / f"{flow}-{py}.yml").exists()
            else []
        ),
    ]
    for (flow, pf, py, lab), target in ENVENTURES.items()
}


[
    ENV_DEPS[flow, pf, py, lab].extend(
        [
            *([ENV_SPECS / f"{py}.yml"] if py else []),
            *([ENV_SPECS / f"{lab}.yml"] if lab else []),
        ]
    )
    for (flow, pf, py, lab), target in ENVENTURES.items()
]

# linting
ALL_ROBOT = [*ATEST.rglob("*.robot"), *ATEST.rglob("*.resource"), *ROBOT_SRC]
ALL_PY = [*SCRIPTS.rglob("*.py"), *PY_SRC, DODO, DOCS_CONF_PY]
ALL_DOCS_SRC = [
    p
    for p in [
        *(DOCS / "_static").rglob("*.*"),
        *DOCS.rglob("*.ipynb"),
        *PY_SRC,
        DOCS_CONF_PY,
    ]
    if ".ipynb_checkpoints" not in str(p)
    and "_robot_magic_" not in str(p)
    and not p.name.endswith(".html")
]

PACKAGE_JSON = ROOT / "package.json"
PACKAGE = safe_load(PACKAGE_JSON.read_text("utf-8"))
YARN_LOCK = ROOT / "yarn.lock"
YARN_INTEGRITY = ROOT / "node_modules" / ".yarn-integrity"
ALL_PRETTIER = [
    *ROOT.glob("*.md"),
    *ROOT.glob("*.json"),
    *ROOT.glob("*.yml"),
    *DOCS.glob("*.yml"),
    *DOCS.rglob("*.css"),
    *GITHUB.rglob("*.yml"),
    *BINDER.rglob("*.yml"),
]

# conda testing
RECIPE = GITHUB / "recipe"
META_YAML_IN = RECIPE / "meta.yaml.in"
META_YAML = GITHUB / "recipe" / "meta.yaml"
CONDA_BLD = DIST / "conda-bld"
CONDA_PKG = (
    CONDA_BLD / "noarch" / f"""{IMPORTABLE.replace("_", "-")}-{VERSION}-py_0.tar.bz2"""
)

ROBOTIDY_ARGS = [
    "robotidy",
    "--configure=ReplaceRunKeywordIf:enabled=False",
    "--target-version=rf4",
]
ROBOCOP_ARGS = [
    "robocop",
    *("--configure", "empty-lines-between-sections:empty_lines:2"),
    *("--exclude", "if-can-be-used"),
    *("--exclude", "deprecated-statement"),
    *("--exclude", "too-many-calls-in-keyword"),
]


class OK:
    atest = BUILD / ".ok.atest"
    black = BUILD / ".ok.black"
    prettier = BUILD / ".ok.prettier"
    pyflakes = BUILD / ".ok.pyflakes"
    robocop = BUILD / ".ok.robocop"
    robot = BUILD / ".ok.robot"
    robot_dry_run = BUILD / ".ok.robot.dryrun"
    robotidy = BUILD / ".ok.robotidy"


def get_atest_stem(attempt=1, extra_args=None, lockfile=None, browser=None):
    """get the directory in ATEST_OUT for this platform/apps"""
    browser = browser or BROWSER
    extra_args = extra_args or []

    if not lockfile:
        lockfile = get_lockfile("test")

    if not lockfile:
        raise RuntimeError(["Couldn't get lockfile", attempt, extra_args, browser])

    stem = None

    for env in ["lint", "test"]:
        try:
            stem = (
                str(lockfile.parent.relative_to(LOCKS / env)) + f"_{attempt}_{browser}"
            )
        except:
            pass

    if not stem:
        raise RuntimeError(["could not get stem", lockfile])

    if "--dryrun" in extra_args:
        stem += "_dry_run"

    return stem


def get_lockfile(env):
    """

    using the POSIX path in .github/locks, e.g.

        RFJL_LOCKDIR=test/linux-64/py3.9/lab3 doit test
    """
    lockfile = None

    env_var_lock = os.environ.get("RFJL_LOCKDIR")

    if env_var_lock is not None:
        eflow, epf, epy, elab = [
            (v if v != "" else None) for v in env_var_lock.split("/")
        ]
        try:
            lockfile = [
                target
                for (flow, pf, py, lab), target in ENVENTURES.items()
                if (flow == env == eflow)
                and (
                    (pf == epf)
                    and (lab == elab if lab else True)
                    and (py == epy if py else True)
                )
            ][-1]
        except:
            pass

    if lockfile is None:
        try:
            lockfile = [
                target
                for (flow, pf, py, lab), target in ENVENTURES.items()
                if flow == env and pf == THIS_CONDA_SUBDIR
            ][-1]
        except:
            return

    return lockfile


def get_ok_actions(p):
    """create a pair of doit `actions` for working with a canary/ok file"""
    return [
        lambda: p.unlink() if p.exists() else None,
        lambda: [p.parent.mkdir(exist_ok=True, parents=True), p.touch(), None][-1],
    ]
