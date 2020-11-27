import subprocess

from . import project as P


def combine():
    final = P.ATEST_OUT / P.ATEST_OUT_XML

    all_robot = [p for p in P.ATEST_OUT.rglob(P.ATEST_OUT_XML) if p != final]
    args = [
        "python",
        "-m",
        "robot.rebot",
        "--name",
        "JupyterLibrary",
        "--outputdir",
        P.ATEST_OUT,
        "--output",
        P.ATEST_OUT_XML,
    ] + all_robot
    proc = subprocess.Popen(args)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    combine()
