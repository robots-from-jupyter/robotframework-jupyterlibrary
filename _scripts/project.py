from pathlib import Path
from ruamel_yaml import safe_load

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
GITHUB = ROOT / ".github"
WORKFLOWS = GITHUB / "workflows"
LOCKS = GITHUB / "locks"

# partial environments
ENV_SPECS = GITHUB / "env_specs"

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
    ("tests", pf, py, lab): LOCKS / "tests" / pf / f"py{py}" / f"lab{lab}" / "conda.lock"
    for pf in PLATFORMS
    for lab in LABS
    for py in PYTHONS
    if not EXCLUDES.get(("tests", pf, py, lab))
}


ENVENTURES.update({
    ("lint", pf, None, None): LOCKS / "lint" / pf / "conda.lock"
    for pf in PLATFORMS
})

ENVENTURES.update({
    ("docs", pf, None, None): LOCKS / "docs" / pf / "conda.lock"
    for pf in PLATFORMS
})

ENV_DEPS = {
    (flow, pf, py, lab): [
        ENV_SPECS / "_base.yml",
        ENV_SPECS / f"{flow}.yml"
    ]
    for (flow, pf, py, lab), target in ENVENTURES.items()
}


[
    ENV_DEPS[flow, pf, py, lab].extend([
        *([ENV_SPECS / f"py_{py}.yml"] if py else []),
        *([ENV_SPECS / f"lab_{lab}.yml"] if lab else []),
    ])
    for (flow, pf, py, lab), target in ENVENTURES.items()
]

PY = ["python"]
PYM = [*PY, "-m"]
SCRIPT_LOCK = [*PYM, "_scripts.lock"]
