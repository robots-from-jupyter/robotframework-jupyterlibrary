import subprocess
import sys
import tempfile
from argparse import ArgumentParser
from pathlib import Path

from conda.models.match_spec import MatchSpec

from . import project as P

parser = ArgumentParser()

CHN = "channels"
DEP = "dependencies"
EXP = "@EXPLICIT"


def expand_specs(specs):
    for raw in specs:
        match = MatchSpec(raw)
        yield match.name, [raw, match]


def merge(composite, env):
    if CHN in env:
        composite[CHN] = env[CHN]

    for channel in env.get(CHN, []):
        if channel not in composite.get(CHN, []):
            composite[CHN] += [channel]

    comp_specs = dict(expand_specs(composite.get(DEP, [])))
    env_specs = dict(expand_specs(env.get(DEP, [])))

    composite[DEP] = [raw for (raw, match) in env_specs.values()] + [
        raw for name, (raw, match) in comp_specs.items() if name not in env_specs
    ]

    return composite


def lock(flow, pf, py, lab):
    output = P.ENVENTURES[flow, pf, py, lab]
    if not output.parent.exists():
        output.parent.mkdir(parents=True)

    env_args = [f"--file={env}" for env in P.ENV_DEPS[flow, pf, py, lab]]

    return_code = -1

    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        for mamba_arg in ["--mamba", "--no-mamba"]:
            args = [
                "conda-lock",
                mamba_arg,
                f"--platform={pf}",
                "--kind=explicit",
                *env_args,
            ]
            print(">>>", " ".join(args), flush=True)
            return_code = subprocess.call(args, cwd=td)
            if return_code == 0:
                if not output.parent.exists():
                    output.parent.mkdir(parents=True)
                output.write_text(
                    "\n".join(
                        [
                            EXP,
                            (tdp / f"conda-{pf}.lock")
                            .read_text()
                            .split(EXP)[1]
                            .strip(),
                        ],
                    ),
                )
                break
    return return_code


def main(lockfile=None):
    lockfile = lockfile or sys.argv[1]
    assert lockfile
    lockpath = Path(lockfile)
    flow, platform, python, lab = [k for k, v in P.ENVENTURES.items() if v == lockpath][
        0
    ]
    return lock(flow, platform, python, lab)


if __name__ == "__main__":
    sys.exit(main())
