import subprocess
import sys
from os.path import abspath, dirname, join

# import for PATH side-effect. yuck.
import chromedriver_binary  # noqa


here = dirname(__file__)
out = abspath(join(here, "..", "_artifacts", "test_output"))
tests = abspath(join(here, "..", "atest", "acceptance"))


def run_tests(*robot_args):
    proc = subprocess.Popen(
        ["python", "-m", "robot", "-d", out, "--xunit", "robot.xunit.xml"]
        + list(robot_args)
        + [tests],
        cwd=here,
    )

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    sys.exit(run_tests(*sys.argv[1:]))
