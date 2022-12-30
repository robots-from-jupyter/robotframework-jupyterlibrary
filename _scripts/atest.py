import subprocess
import sys
import os
import shutil
import time

from . import project as P


PLATFORM_PY_ARGS = {
    # e.g. if notebook and ipykernel releases did not yet support python 5.0 with lab 6
    # ("Windows", "5.0", "6"): ["--include", "not-supported", "--runemptysuite"]
}

LAB_MAJOR_ENV_VARS = {
    1: {"JUPYTER_LIBRARY_APP": "NotebookApp"},
    2: {"JUPYTER_LIBRARY_APP": "NotebookApp"},
    3: {"JUPYTER_LIBRARY_APP": "ServerApp"},
}

NON_CRITICAL = [
    ## Historically supported nteract_on_jupyter
    # ["client:nteract_on_jupyter"],
]

PABOT_DEFAULTS = [
    "--testlevelsplit",
    *("--processes", "4"),
    "--artifactsinsubfolders",
    *("--artifacts", "png,log,txt"),
]


def run_tests(attempt=0, extra_args=None):
    env = dict(**os.environ)

    if P.THIS_LAB:
        lab_major = int(P.THIS_LAB.split(".")[0])
        env.update(LAB_MAJOR_ENV_VARS.get(lab_major, {}))

    extra_args = extra_args or []
    extra_args += PLATFORM_PY_ARGS.get((P.PLATFORM, P.THIS_PYTHON, P.THIS_LAB), [])

    stem = P.get_atest_stem(attempt=attempt, extra_args=extra_args)
    out_dir = P.ATEST_OUT / stem

    for non_critical in NON_CRITICAL:
        extra_args += ["--noncritical", "AND".join(non_critical)]

    log_level = "INFO"
    if attempt > 1:
        log_level = "TRACE"
        prev_stem = P.get_atest_stem(attempt=attempt - 1, extra_args=extra_args)
        previous = P.ATEST_OUT / prev_stem / P.ATEST_OUT_XML
        if previous.exists():
            extra_args += ["--rerunfailed", str(previous)]

    runner = ["pabot", *PABOT_DEFAULTS]

    if "--dryrun" in extra_args:
        runner = ["robot"]

    args = [
        *runner,
        *extra_args,
        "--loglevel",
        log_level,
        "--name",
        f"""{P.PLATFORM} py{P.THIS_PYTHON} lab{P.THIS_LAB.split(".")[0]}""",
        "--outputdir",
        out_dir,
        "--variable",
        f"BROWSER:{P.BROWSER}",
        "--variable",
        f"OS:{P.PLATFORM}",
        "--variable",
        f"LAB:{P.THIS_LAB}",
        "--variable",
        f"PY:{P.THIS_PYTHON}",
        "--randomize",
        "all",
        "--xunit",
        ".".join(["xunit", "xml"]),
        ".",
    ]

    if out_dir.exists():
        print(f">>> trying to clean out {out_dir}", flush=True)
        try:
            shutil.rmtree(out_dir)
        except Exception as err:
            print(
                f"... error, hopefully harmless: {err}",
                flush=True,
            )

    if not out_dir.exists():
        print(f">>> trying to prepare output directory: {out_dir}", flush=True)
        try:
            out_dir.mkdir(parents=True)
        except Exception as err:
            print(
                f"... Error, hopefully harmless: {err}",
                flush=True,
            )

    str_args = [*map(str, args)]
    print(">>> ", " ".join(str_args), flush=True)

    proc = subprocess.Popen(str_args, cwd=P.ATEST, env=env)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


def attempt_atest_with_retries(extra_args=None):
    """retry the robot tests a number of times"""
    extra_args = list(extra_args or [])
    attempt = 0
    error_count = -1

    retries = int(os.environ.get("ATEST_RETRIES") or "0")
    extra_args += os.environ.get("ATEST_ARGS", "").split()

    while error_count != 0 and attempt <= retries:
        attempt += 1
        print(f"attempt {attempt} of {retries + 1}...", flush=True)
        start_time = time.time()
        error_count = run_tests(attempt=attempt, extra_args=extra_args)
        print(
            error_count,
            "errors in",
            int(time.time() - start_time),
            "seconds",
            flush=True,
        )

    return error_count


if __name__ == "__main__":
    sys.exit(attempt_atest_with_retries(extra_args=sys.argv[1:]))
