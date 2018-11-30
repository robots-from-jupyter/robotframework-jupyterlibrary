import sys
import subprocess
import os

here = os.path.dirname(__file__)
out = os.path.join(here, "..", "_artifacts", "test_output")
tests = os.path.join(here, "acceptance")


def run_tests(*robot_args):
    return subprocess.check_call([
        "python", "-m", "robot", "-d", out, tests
    ], cwd=here)


if __name__ == "__main__":
    sys.exit(run_tests(sys.argv[1:]))
