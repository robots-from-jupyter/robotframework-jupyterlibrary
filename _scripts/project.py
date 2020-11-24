from pathlib import Path
from ruamel_yaml import safe_load
import platform

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
ALL_PY = [*SCRIPTS.rglob("*.py"), *PY_SRC, DODO]
ATEST = ROOT / "atest"
ROBOT_SRC = [*SRC.rglob("*.robot")]
ALL_ROBOT = [*ATEST.rglob("*.robot"), *ROBOT_SRC]

BUILD = ROOT / "build"
BUILD.exists() or BUILD.mkdir()

DIST = ROOT / "dist"
IMPORTABLE = "robotframework_jupyterlibrary"
SDIST = DIST / f"""{IMPORTABLE.replace("_", "-")}-{VERSION}.tar.gz"""
WHEEL = DIST / f"{IMPORTABLE}-{VERSION}-py3-none-any.whl"

# partial environments
GITHUB = ROOT / ".github"
WORKFLOWS = GITHUB / "workflows"
LOCKS = GITHUB / "locks"
ENV_SPECS = GITHUB / "env_specs"
ENVS = ROOT / ".envs"

ENV_NAMES = ["tests", "lint", "docs"]
RUN_IN = {env: ["conda", "run", "-p", ENVS / env] for env in ENV_NAMES}

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
