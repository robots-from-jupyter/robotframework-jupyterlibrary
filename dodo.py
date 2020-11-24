import os
import subprocess

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


def task_build():
    yield dict(name="pypi", actions=[[*P.PY, "setup.py", "sdist", "bdist_wheel"]])


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

    yield dict(
        name=env,
        file_dep=[lockfile],
        actions=[
            lambda: explicit_list.unlink() if explicit_list.exists() else None,
            ["conda", "create", "-yp", P.ENVS / env, "--file", lockfile],
            lambda: [
                explicit_list.write_bytes(
                    subprocess.check_output(
                        ["conda", "list", "--explicit", "--md5", "-p", P.ENVS / env]
                    )
                ),
                None,
            ][-1],
        ],
        targets=[explicit_list],
    )


def task_env():
    for env in ["tests", "lint", "docs"]:
        task = _make_env(env)
        if task:
            yield task


def task_lint():
    env_lock = P.BUILD / "lint" / "conda.lock"
    yield dict(
        name="black",
        actions=[[*P.RUN_IN["lint"], *P.PYM, "black", *P.ALL_PY]],
        file_dep=[*P.ALL_PY, env_lock],
    )
    yield dict(
        name="pyflakes",
        actions=[[*P.RUN_IN["lint"], *P.PYM, "pyflakes", *P.ALL_PY]],
        file_dep=[*P.ALL_PY, env_lock],
    )
    yield dict(
        name="robot:tidy",
        actions=[
            [*P.RUN_IN["lint"], *P.PYM, "robot.tidy", "--recursive", it]
            for it in [P.SRC, P.ATEST]
        ],
        file_dep=[*P.ALL_ROBOT],
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
