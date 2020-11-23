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

ENVENTURES = {
    (pf, py, lab): LOCKS / pf / f"py{py}" / f"lab{lab}" / "conda.lock"
    for pf in PLATFORMS
    for lab in LABS
    for py in PYTHONS
}

ENV_DEPS = {
    (pf, py, lab): [
        ENV_SPECS / "_base.yml",
    ]
    for (pf, py, lab), target in ENVENTURES.items()
}


[
    ENV_DEPS[pf, py, lab].extend([
        ENV_SPECS / f"py_{py}.yml",
        ENV_SPECS / f"lab_{lab}.yml",
    ])
    for (pf, py, lab), target in ENVENTURES.items()
]



PYM = ["python", "-m"]
SCRIPT_LOCK = [*PYM, "_scripts.lock"]
