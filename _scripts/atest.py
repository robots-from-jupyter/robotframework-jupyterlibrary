import subprocess
import sys
import os

# import for PATH side-effect. yuck.
# import chromedriver_binary  # noqa

from . import BROWSER, ROOT, PLATFORM, TESTS, TEST_OUT

NON_CRITICAL = [
    ## Historically supported nteract_on_jupyter
    # ["client:nteract_on_jupyter"],
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
            "--variable",
            f"BROWSER:{BROWSER}",
            "--variable",
            f"OS:{PLATFORM}",
            "--xunit",
            ".".join(["xunit", "xml"]),
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
