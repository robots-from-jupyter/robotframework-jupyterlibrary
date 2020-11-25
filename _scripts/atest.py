import subprocess
import sys
import os
from os.path import join

# import for PATH side-effect. yuck.
# import chromedriver_binary  # noqa

from . import BROWSER, ROOT, PLATFORM, TESTS, TEST_OUT

NON_CRITICAL = [
    # TODO: figure out some plan for supporting obfuscated nteract
    ["client:nteract_on_jupyter"],
]


def run_tests(robot_args):
    for non_critical in NON_CRITICAL:
        robot_args += ["--noncritical", "AND".join(non_critical)]

    args = (
        [
            "pabot",
            "--testlevelsplit",
            "--artifactsinsubfolders",
            "-d",
            TEST_OUT,
            "--log",
            join(".".join([PLATFORM, BROWSER, "log", "html"])),
            "--name",
            "{} on {}".format(BROWSER, PLATFORM),
            "--output",
            join(".".join([PLATFORM, BROWSER, "robot", "xml"])),
            "--report",
            join(".".join([PLATFORM, BROWSER, "report", "html"])),
            "--variable",
            "BROWSER:" + BROWSER,
            "--variable",
            "OS:" + PLATFORM,
            "--xunit",
            ".".join([PLATFORM, BROWSER, "robot", "xunit", "xml"]),
        ]
        + robot_args
        + [TESTS]
    )

    print(" ".join(args), flush=True)
    proc = subprocess.Popen(args, cwd=ROOT)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    sys.exit(run_tests([*sys.argv[1:], *os.environ.get("ATEST_ARGS", "").split()]))
