import os
import shutil
import subprocess
import sys
import time

from . import project as P

PLATFORM_PY_ARGS = {
    # e.g. if notebook and ipykernel releases did not yet support python 5.0 with lab 6
}

LAB_MAJOR_ENV_VARS = {
    1: {"JUPYTER_LIBRARY_APP": "NotebookApp"},
    2: {"JUPYTER_LIBRARY_APP": "NotebookApp"},
}

LAB_MAJOR_ARGS = {
    4: ["--exclude=client:classic"],
    3: ["--exclude=client:notebook"],
}

NON_CRITICAL = [
    ## Historically supported nteract_on_jupyter
]

PABOT_DEFAULTS = [
    "--testlevelsplit",
    *("--processes", "4"),
    "--artifactsinsubfolders",
    *("--artifacts", "png,log,txt"),
]


def run_tests(attempt=0, extra_args=None):
    env = dict(**os.environ)

    extra_args = extra_args or []
    extra_args += PLATFORM_PY_ARGS.get((P.PLATFORM, P.THIS_PYTHON, P.THIS_LAB), [])

    if P.THIS_LAB:
        lab_major = int(P.THIS_LAB.split(".")[0])
        env.update(LAB_MAJOR_ENV_VARS.get(lab_major, {}))
        extra_args += LAB_MAJOR_ARGS.get(lab_major, [])

    stem = P.get_atest_stem(attempt=attempt, extra_args=extra_args)
    out_dir = P.ATEST_OUT / stem
    cov_dir = out_dir / "coverage"

    for non_critical in NON_CRITICAL:
        extra_args += ["--noncritical", "AND".join(non_critical)]

    log_level = "INFO"
    if attempt > 1:
        log_level = "TRACE"
        prev_stem = P.get_atest_stem(attempt=attempt - 1, extra_args=extra_args)
        previous = P.ATEST_OUT / prev_stem / P.ATEST_OUT_XML
        if previous.exists():
            extra_args += ["--rerunfailed", str(previous)]

    if "--dryrun" in extra_args:
        runner = ["robot"]
    else:
        runner = [
            "pabot",
            *PABOT_DEFAULTS,
            "--command",
            "coverage",
            "run",
            "--branch",
            "--source=JupyterLibrary,SeleniumLibrary,selenium",
            "--parallel-mode",
            f"--context=atest-{P.PLATFORM}-{P.THIS_PYTHON}-{P.THIS_LAB}-{P.BROWSER}-{attempt}",
            f"--data-file={out_dir}/coverage/.coverage",
            "-m",
            "robot",
            "--end-command",
        ]

    args = [
        *runner,
        *extra_args,
        "--loglevel",
        log_level,
        "--name",
        "JupyterLibrary",
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
        "--variable",
        f"ATTEMPT:{attempt}",
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
            cov_dir.mkdir(parents=True)
        except Exception as err:
            print(
                f"... Error, hopefully harmless: {err}",
                flush=True,
            )

    str_args = [*map(str, args)]
    print(">>> ", " ".join(str_args), flush=True)

    proc = subprocess.Popen(str_args, cwd=P.ATEST, env=env)

    return_code = None
    try:
        return_code = proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return_code = proc.wait()

    if return_code != 0:
        for robot_stdout in out_dir.rglob("robot_stdout.out"):
            out_text = robot_stdout.read_text(encoding="utf-8")
            if "FAIL" in out_text:
                print("\n", robot_stdout, "\n")
                print(out_text, "\n", "\n", flush=True)

    print("Log:", (out_dir / "log.html").as_uri())

    return return_code


def attempt_atest_with_retries(extra_args=None):
    """Retry the robot tests a number of times."""
    extra_args = list(extra_args or [])
    error_count = -1

    if "--dryrun" in extra_args:
        attempt = 0
        retries = 0
    else:
        attempt = int(os.environ.get("ATEST_ATTEMPT") or "0")
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
