from pathlib import Path

import platform
import os
import sys

try:
    __import__("conda_lock")
    CAN_CONDA_LOCK = True
except:
    CAN_CONDA_LOCK = False

for _yaml in ["yaml", "ruamel_yaml", "ruamel.yaml"]:
    try:
        yaml = __import__(_yaml)
        if _yaml == "ruamel.yaml":
            safe_load = yaml.yaml.safe_load
        else:
            safe_load = yaml.safe_load
    except ImportError:
        pass

assert safe_load, "need at least a yaml parser"


CI = int(os.environ.get("CI", "0"))
BINDER = int(os.environ.get("BINDER", "0"))
PLATFORM = platform.system()
BROWSER = os.environ.get("BROWSER", "headlessfirefox")

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
VERSION = VERSION_FILE.read_text().strip()
PY_SRC = [*SRC.rglob("*.py")]
SETUP_CRUFT = [
    ROOT / "setup.py",
    ROOT / "MANIFEST.in",
    ROOT / "setup.cfg",
    VERSION_FILE,
]

ATEST = ROOT / "atest"
ROBOT_SRC = [*SRC.rglob("*.robot")]

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
DOCS_CONF_PY = DOCS / "conf.py"
DOCS_BUILDINFO = BUILD / "docs" / "html" / ".buildinfo"

# partial environments
GITHUB = ROOT / ".github"
WORKFLOWS = GITHUB / "workflows"
LOCKS = GITHUB / "locks"
ENV_SPECS = GITHUB / "env_specs"
ENVS = ROOT / ".envs"

ENV_NAMES = ["test", "lint", "docs"]

CONDA_RUN = [CONDA_EXE, "run"]
if CI:
    RUN_IN = {env: [*CONDA_RUN, "-n", env] for env in ENV_NAMES}
else:
    RUN_IN = {
        env: [*CONDA_RUN, "--live-stream", "--no-capture-output", "-p", ENVS / env]
        for env in ENV_NAMES
    }

CONDA_LISTS = {env: BUILD / env / "conda.lock" for env in ENV_NAMES}
PIP_LISTS = {env: BUILD / env / "pip.freeze" for env in ENV_NAMES}

WORKFLOW_CI = WORKFLOWS / "ci.yml"
WORKFLOW_CI_YAML = safe_load(WORKFLOW_CI.read_text())
TEST_MATRIX = WORKFLOW_CI_YAML["jobs"]["test"]["strategy"]["matrix"]
PYTHONS = TEST_MATRIX["python-version"]
LABS = TEST_MATRIX["lab-version"]
PLATFORMS = TEST_MATRIX["conda-subdir"]

EXCLUDES = {
    ("test", ex["conda-subdir"], ex["python-version"], ex["lab-version"]): True
    for ex in TEST_MATRIX.get("exclude", [])
}

ENVENTURES = {
    ("test", pf, py, lab): LOCKS / "test" / pf / py / lab / "conda.lock"
    for pf in PLATFORMS
    for lab in LABS
    for py in PYTHONS
    if not EXCLUDES.get(("test", pf, py, lab))
}


ENVENTURES.update(
    {("lint", pf, None, None): LOCKS / "lint" / pf / "conda.lock" for pf in PLATFORMS}
)

ENVENTURES.update(
    {("docs", pf, None, None): LOCKS / "docs" / pf / "conda.lock" for pf in PLATFORMS}
)

ENV_DEPS = {
    (flow, pf, py, lab): [
        ENV_SPECS / "_base.yml",
        ENV_SPECS / f"{flow}.yml",
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
ALL_ROBOT = [*ATEST.rglob("*.robot"), *ROBOT_SRC]
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
]


def get_atest_stem(attempt=1, extra_args=None, lockfile=None, browser=None):
    """get the directory in ATEST_OUT for this platform/apps"""
    browser = browser or BROWSER
    extra_args = extra_args or []

    if not lockfile:
        lockfile = get_lockfile("test")

    stem = str(lockfile.parent.relative_to(LOCKS / "test")) + f"_{attempt}_{browser}"

    if "--dryrun" in extra_args:
        stem += "_dry_run"

    return stem


def get_lockfile(env):
    lockfile = None

    env_var_lock = os.environ.get("RFJL_LOCKFILE")

    if env_var_lock is not None:
        eflow, epf, epy, elab = [
            (v if v != "" else None) for v in env_var_lock.split(":")
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
