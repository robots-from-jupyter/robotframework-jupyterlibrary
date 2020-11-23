from pathlib import Path

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent
LOCKS = ROOT / "locks"

# partial environments
ENV_SPECS = ROOT / "_env_specs"

PYTHONS = ["3.6", "3.7", "3.8"]
LABS = ["1", "2"]
PLATFORMS = ["win-64", "linux-64", "osx-64"]

ENVENTURES = {
    (pf, py, lab): LOCKS / (f"{pf}-py{py}-lab{lab}".replace(".", "_") + ".conda.lock")
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

# [
#     ENV_DEPS[pf, py, lab].append(ENV_SPECS / f"lab_{lab}.yml")
#     for (pf, py, lab), target in ENVENTURES.items()
# ]
[
    ENV_DEPS[pf, py, lab].append(ENV_SPECS / f"py_{py}.yml")
    for (pf, py, lab), target in ENVENTURES.items()
]
