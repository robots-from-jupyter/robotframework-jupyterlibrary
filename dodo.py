import os
import subprocess

from doit.tools import PythonInteractiveAction, config_changed

from _scripts import project as P

os.environ["PYTHONIOENCODING"] = "utf-8"

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
}


def task_binder():
    """get to a basic interactive state"""
    return dict(actions=[["echo", "ok"]])


def task_release():
    return dict(actions=[["echo", "ok"]], task_dep=["lint", "docs", "build", "test"])


def task_build():
    yield dict(
        name="pypi",
        actions=[[*P.PY, "setup.py", "sdist", "bdist_wheel"]],
        targets=[P.SDIST, P.WHEEL],
        file_dep=[*P.PY_SRC, *P.ROBOT_SRC, P.VERSION_FILE, *P.SETUP_CRUFT],
    )


def task_docs():
    env = "docs"
    run_in = P.RUN_IN[env]
    frozen = P.PIP_LISTS[env]

    yield dict(
        name="sphinx",
        actions=[[*run_in, "sphinx-build", "-M", "html", "docs", "build/docs"]],
        file_dep=[frozen, *P.ALL_DOCS_SRC, *P.SETUP_CRUFT],
        targets=[P.DOCS_BUILDINFO],
    )


def _make_env(env):
    try:
        lockfile = [
            target
            for (flow, pf, py, lab), target in P.ENVENTURES.items()
            if flow == env and pf == P.THIS_CONDA_SUBDIR
        ][-1]
    except:
        return

    explicit_list = P.BUILD / env / lockfile.name

    if not explicit_list.parent.exists():
        explicit_list.parent.mkdir(parents=True)

    actions = [
        lambda: explicit_list.unlink() if explicit_list.exists() else None,
    ]

    if P.CI:
        env_args = ["-n", env]
    else:
        env_args = ["-p", P.ENVS / env]
        actions += [
            ["conda", "create", "-y", *env_args, "--file", lockfile],
        ]
    actions += [
        lambda: [
            explicit_list.write_bytes(
                subprocess.check_output(
                    ["conda", "list", "--explicit", "--md5", *env_args]
                )
            ),
            None,
        ][-1],
    ]

    yield dict(
        name=env,
        file_dep=[lockfile],
        actions=actions,
        targets=[explicit_list],
    )


def task_env():
    for env in ["tests", "lint", "docs"]:
        task = _make_env(env)
        if task:
            yield task


def task_lint():
    env = "lint"
    env_lock = P.CONDA_LISTS["lint"]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]

    yield dict(
        name="black",
        actions=[[*pym, "black", "--quiet", *P.ALL_PY]],
        file_dep=[*P.ALL_PY, env_lock],
    )

    yield dict(
        name="pyflakes",
        task_dep=["lint:black"],
        actions=[[*pym, "pyflakes", *P.ALL_PY]],
        file_dep=[*P.ALL_PY, env_lock],
    )

    yield dict(
        name="robot:tidy",
        actions=[[*pym, "robot.tidy", "--recursive", it] for it in [P.SRC, P.ATEST]],
        file_dep=[*P.ALL_ROBOT, env_lock],
    )


def task_lab():
    """start jupyter_lab (and other extensions)"""

    env = "tests"
    frozen = P.PIP_LISTS[env]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]

    def _lab():
        p = subprocess.Popen(
            [*pym, "jupyter", "lab", "--no-browser", "--debug"], stdin=subprocess.PIPE
        )
        try:
            p.wait()
        except KeyboardInterrupt:
            p.terminate()
            p.communicate(b"y\n")
            p.terminate()
        finally:
            p.wait()

        print("maybe check your process log")

    yield dict(
        name="serve",
        uptodate=[lambda: False],
        actions=[PythonInteractiveAction(_lab)],
        file_dep=[frozen],
    )


def _make_setup(env):
    frozen = P.PIP_LISTS[env]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]

    yield dict(
        name=env,
        actions=[
            [
                *pym,
                "pip",
                "install",
                "-e",
                ".",
                "--no-deps",
                "--ignore-installed",
            ],
            [*pym, "pip", "check"],
            lambda: [
                frozen.write_bytes(subprocess.check_output([*pym, "pip", "freeze"])),
                None,
            ][-1],
        ],
        file_dep=[P.CONDA_LISTS[env]],
        targets=[frozen],
    )


def task_setup():
    for env in ["tests", "docs"]:
        yield _make_setup(env)


def task_test():
    env = "tests"

    yield dict(
        name="atest",
        uptodate=[config_changed(os.environ.get("ATEST_ARGS", ""))],
        actions=[[*P.RUN_IN[env], *P.PYM, "_scripts.atest"]],
        file_dep=[*P.PY_SRC, *P.ALL_ROBOT, P.PIP_LISTS[env]],
        targets=["build/test_output/log.xml"],
    )


def task_lock():
    """generate conda lock files for all the excursions"""
    for (flow, pf, py, lab), target in P.ENVENTURES.items():
        file_dep = P.ENV_DEPS[flow, pf, py, lab]
        yield dict(
            name=f"{flow}_{pf}__py{py}__lab{lab}".replace(".", "_"),
            actions=[[*P.SCRIPT_LOCK, target]],
            file_dep=file_dep,
            targets=[target],
        )
