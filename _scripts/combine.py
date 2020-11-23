import subprocess
from glob import glob
from os.path import join

from . import HERE, TEST_OUT


def combine():
    args = [
        "python",
        "-m",
        "robot.rebot",
        "--name",
        "JupyterLibrary",
        "--outputdir",
        TEST_OUT,
        "--output",
        "output.xml",
    ] + list(glob(join(TEST_OUT, "*.robot.xml")))
    proc = subprocess.Popen(args, cwd=HERE)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    combine()
