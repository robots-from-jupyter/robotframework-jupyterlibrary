import sys
import subprocess

from . import project as P


def combine():
    final = P.ATEST_OUT / P.ATEST_OUT_XML

    all_files = [*P.ATEST_OUT.rglob(P.ATEST_OUT_XML)]
    print(all_files)

    all_robot = [
        p
        for p in P.ATEST_OUT.rglob(P.ATEST_OUT_XML)
        if p != final and "pabot_results" not in str(p)
    ]
    args = [
        "python",
        "-m",
        "robot.rebot",
        "--outputdir",
        P.ATEST_OUT,
        "--output",
        P.ATEST_OUT_XML,
    ] + all_robot

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
