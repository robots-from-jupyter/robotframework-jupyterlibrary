import subprocess
import sys

from . import project as P


def combine():
    final = P.ATEST_OUT / P.ATEST_OUT_XML

    all_robot = [
        p
        for p in P.ATEST_OUT.rglob(P.ATEST_OUT_XML)
        if p != final and "dry_run" not in str(p) and "pabot_results" not in str(p)
    ]
    print(f"all {P.ATEST_OUT_XML} in {P.ATEST_OUT}", flush=True)
    [print(f"- {p.relative_to(P.ATEST_OUT)}", flush=True) for p in all_robot]

    args = [
        "python",
        "-m",
        "robot.rebot",
        "--name",
        "🤖",
        "--nostatusrc",
        "--merge",
        *all_robot,
    ]

    str_args = [*map(str, args)]

    print(">>> rebot args: ", " ".join(str_args), flush=True)

    proc = subprocess.Popen(str_args)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    sys.exit(combine())
