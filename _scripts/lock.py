import sys
from pathlib import Path
from . import project as P
import subprocess
import tempfile
from conda.models.match_spec import MatchSpec
from argparse import ArgumentParser

from ruamel_yaml import safe_load, safe_dump

parser = ArgumentParser()
parser.add_argument('--platform', help='the platform')
parser.add_argument('--python', help='the version of python')
parser.add_argument('--lab', help='the version of jupyterlab')

CHN = "channels"
DEP = "dependencies"

def expand_specs(specs):
    for raw in specs:
        match = MatchSpec(raw)
        yield match.name, [raw, match]

def merge(composite, env):
    for channel in env.get(CHN, []):
        if channel not in composite.get(CHN, []):
            composite[CHN] = [channel, *composite.get(CHN, [])]

    comp_specs = dict(expand_specs(composite.get(DEP, [])))
    env_specs = dict(expand_specs(env.get(DEP, [])))

    composite[DEP] = [
        raw for (raw, match) in env_specs.values()
    ] + [
        raw for name, (raw, match) in comp_specs.items() if name not in env_specs
    ]

    return composite


def lock(pf, py, lab):
    output = P.ENVENTURES[pf, py, lab]
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    composite = {"name": output.name, CHN: [], DEP: []}
    for env in P.ENV_DEPS[pf, py, lab]:
        composite = merge(composite, safe_load(env.read_text()))

    print(safe_dump(composite, default_flow_style=False), flush=True)

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        env = tdp / "environment.yml"
        env.write_text(safe_dump(composite, default_flow_style=False))
        args = ["conda", "lock", "--platform", pf]
        subprocess.check_call(args, cwd=td)
        if not output.parent.exists():
            output.parent.mkdir(parents=True)
        output.write_text((tdp / f"conda-{pf}.lock").read_text())
    return 0


def main(platform=None, python=None, lab=None):
    args = parser.parse_args()
    platform = platform or args.platform
    python = python or args.python
    lab = lab or args.lab
    assert (platform, python, lab) in P.ENVENTURES
    return lock(platform, python, lab)


if __name__ == "__main__":
    sys.exit(main())
