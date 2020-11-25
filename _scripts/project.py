from pathlib import Path

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

import platform
import os

CI = int(os.environ.get("CI", "0"))

THIS_CONDA_SUBDIR = {
    "Linux": "linux-64",
    "Darwin": "osx-64",
    "Windows": "win-64",
}[platform.system()]

# commands
PY = ["python"]
PYM = [*PY, "-m"]
SCRIPT_LOCK = [*PYM, "_scripts.lock"]


SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
DODO = ROOT / "dodo.py"

SETUP_CRUFT = [ROOT / "setup.py", ROOT / "MANIFEST.in", ROOT / "setup.cfg"]

SRC = ROOT / "src" / "JupyterLibrary"
VERSION_FILE = SRC / "VERSION"
VERSION = VERSION_FILE.read_text().strip()
PY_SRC = [*SRC.rglob("*.py")]
ATEST = ROOT / "atest"
ROBOT_SRC = [*SRC.rglob("*.robot")]

BUILD = ROOT / "build"
BUILD.exists() or BUILD.mkdir()

DIST = ROOT / "dist"
IMPORTABLE = "robotframework_jupyterlibrary"
SDIST = DIST / f"""{IMPORTABLE.replace("_", "-")}-{VERSION}.tar.gz"""
WHEEL = DIST / f"{IMPORTABLE}-{VERSION}-py3-none-any.whl"

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

ENV_NAMES = ["tests", "lint", "docs"]

if CI:
    RUN_IN = {env: ["conda", "run", "-n", env] for env in ENV_NAMES}
else:
    RUN_IN = {env: ["conda", "run", "-p", ENVS / env] for env in ENV_NAMES}
CONDA_LISTS = {env: BUILD / env / "conda.lock" for env in ENV_NAMES}
PIP_LISTS = {env: BUILD / env / "pip.freeze" for env in ENV_NAMES}

WORKFLOW_TEST = WORKFLOWS / "tests.yml"
WORKFLOW_TEST_YAML = safe_load(WORKFLOW_TEST.read_text())
TEST_MATRIX = WORKFLOW_TEST_YAML["jobs"]["test"]["strategy"]["matrix"]
PYTHONS = TEST_MATRIX["python-version"]
LABS = TEST_MATRIX["lab-version"]
PLATFORMS = TEST_MATRIX["conda-subdir"]

EXCLUDES = {
    ("tests", ex["conda-subdir"], ex["python-version"], ex["lab-version"]): True
    for ex in TEST_MATRIX.get("exclude", [])
}

ENVENTURES = {
    ("tests", pf, py, lab): LOCKS
    / "tests"
    / pf
    / f"py{py}"
    / f"lab{lab}"
    / "conda.lock"
    for pf in PLATFORMS
    for lab in LABS
    for py in PYTHONS
    if not EXCLUDES.get(("tests", pf, py, lab))
}


ENVENTURES.update(
    {("lint", pf, None, None): LOCKS / "lint" / pf / "conda.lock" for pf in PLATFORMS}
)

ENVENTURES.update(
    {("docs", pf, None, None): LOCKS / "docs" / pf / "conda.lock" for pf in PLATFORMS}
)

ENV_DEPS = {
    (flow, pf, py, lab): [ENV_SPECS / "_base.yml", ENV_SPECS / f"{flow}.yml"]
    for (flow, pf, py, lab), target in ENVENTURES.items()
}


[
    ENV_DEPS[flow, pf, py, lab].extend(
        [
            *([ENV_SPECS / f"py_{py}.yml"] if py else []),
            *([ENV_SPECS / f"lab_{lab}.yml"] if lab else []),
        ]
    )
    for (flow, pf, py, lab), target in ENVENTURES.items()
]

# linting
ALL_ROBOT = [*ATEST.rglob("*.robot"), *ROBOT_SRC]
ALL_PY = [*SCRIPTS.rglob("*.py"), *PY_SRC, DODO, DOCS_CONF_PY]
ALL_DOCS_SRC = [
    *(DOCS / "_static").rglob("*.*"),
    *DOCS.rglob(".ipynb"),
    *PY_SRC,
    DOCS_CONF_PY,
]
