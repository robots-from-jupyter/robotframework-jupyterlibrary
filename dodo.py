import os
import subprocess

from hashlib import sha256

import doit
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
    return dict(actions=[["echo", "ok"]], file_dep=[P.PIP_LISTS["test"]])


def task_release():
    """the full set of tasks needed for a new release"""
    return dict(
        actions=[["echo", "ok"]],
        task_dep=["lint", "test"],
        file_dep=[P.SHA256SUMS, P.DOCS_BUILDINFO],
    )


def task_build():
    """build packages"""
    yield dict(
        name="pypi",
        actions=[[*P.PY, "setup.py", "sdist", "bdist_wheel"]],
        targets=[P.SDIST, P.WHEEL],
        file_dep=[*P.PY_SRC, *P.ROBOT_SRC, P.VERSION_FILE, *P.SETUP_CRUFT],
    )

    def _run_hash():
        # mimic sha256sum CLI
        if P.SHA256SUMS.exists():
            P.SHA256SUMS.unlink()

        lines = []

        for p in P.HASH_DEPS:
            lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

        output = "\n".join(lines)
        print(output)
        P.SHA256SUMS.write_text(output)

    yield dict(
        name="hash",
        file_dep=P.HASH_DEPS,
        targets=[P.SHA256SUMS],
        actions=[_run_hash],
    )


def task_docs():
    """build HTML docs"""
    env = "docs"
    run_in = P.RUN_IN[env]
    frozen = P.PIP_LISTS[env]

    yield dict(
        name="sphinx",
        actions=[[*run_in, "sphinx-build", "-M", "html", "docs", "build/docs"]],
        file_dep=[frozen, *P.ALL_DOCS_SRC, *P.SETUP_CRUFT, *P.ROBOT_SRC],
        targets=[P.DOCS_BUILDINFO],
    )


def _make_env(env):
    lockfile = P.get_lockfile(env)

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
            [P.CONDA_EXE, "create", "-y", *env_args, "--file", lockfile],
        ]
    actions += [
        lambda: [
            explicit_list.write_bytes(
                subprocess.check_output(
                    [P.CONDA_EXE, "list", "--explicit", "--md5", *env_args]
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
    """prepare envs"""
    for env in P.ENV_NAMES:
        task = _make_env(env)
        if task:
            yield task


def task_lint():
    """lint code"""
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

    yield dict(
        name="prettier",
        actions=[
            [*run_in, "yarn", "--silent", "prettier"],
        ],
        file_dep=[*P.ALL_PRETTIER, P.YARN_INTEGRITY],
    )


def task_js():
    env = "lint"

    run_in = P.RUN_IN[env]
    env_lock = P.CONDA_LISTS[env]

    yield dict(
        name="yarn",
        uptodate=[
            config_changed({k: P.PACKAGE[k] for k in ["devDependencies", "prettier"]})
        ],
        file_dep=[P.YARN_LOCK, env_lock],
        actions=[
            [*run_in, "yarn", "--silent", "--prefer-offline", "--ignore-optional"],
        ],
        targets=[P.YARN_INTEGRITY],
    )


def task_lab():
    """start a jupyter lab server (with all other extensions)"""

    env = "test"
    lockfile = P.get_lockfile(env)
    str_lock = str(lockfile)
    needs_build = "lab1" in str_lock or "lab2" in str_lock

    frozen = P.PIP_LISTS[env]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]

    app_dir = []

    if needs_build and not P.IN_BINDER:
        app_dir = ["--app-dir", P.APP_DIR]

    lab = [*pym, "jupyter", "lab"]

    lab_ext = [*pym, "jupyter", "labextension"]

    serve_deps = [frozen]

    if needs_build:
        yield dict(
            name="ext",
            uptodate=[config_changed({"labextensions": P.LAB_EXTENSIONS})],
            actions=[
                [*lab_ext, "install", *app_dir, *P.LAB_EXTENSIONS, "--no-build"],
                [*lab, "build", *app_dir, "--debug"],
            ],
            file_dep=[frozen],
            targets=[P.APP_INDEX],
        )
        serve_deps += [P.APP_INDEX]

    def _lab():
        p = subprocess.Popen(
            [*lab, *app_dir, "--no-browser", "--debug"], stdin=subprocess.PIPE
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
        file_dep=serve_deps,
    )


def _make_setup(env):
    frozen = P.PIP_LISTS[env]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]
    file_dep = [P.CONDA_LISTS[env], *P.SETUP_CRUFT]

    if P.INSTALL_ARTIFACT:
        pip_args = [
            "--no-index",
            "--find-links",
            P.DIST,
            P.SETUP["metadata"]["name"],
        ]
    else:
        pip_args = ["-e", "."]

    yield dict(
        name=env,
        actions=[
            lambda: frozen.unlink() if frozen.exists() else None,
            [*pym, "pip", "install", "--no-deps", "--ignore-installed", *pip_args],
            [*pym, "pip", "check"],
            lambda: [
                frozen.write_bytes(subprocess.check_output([*pym, "pip", "freeze"])),
                None,
            ][-1],
        ],
        targets=[frozen],
        file_dep=file_dep,
    )


def task_setup():
    """do an editable install of the package"""
    for env in P.ENV_NAMES:
        yield _make_setup(env)


def task_test():
    """run tests"""
    env = "test"
    pym = [*P.RUN_IN[env], *P.PYM]

    stem = P.get_atest_stem(lockfile=P.get_lockfile(env), browser=P.BROWSER)

    yield dict(
        name="atest",
        uptodate=[config_changed(os.environ.get("ATEST_ARGS", ""))],
        actions=[[*pym, "_scripts.atest"]],
        file_dep=[*P.PY_SRC, *P.ALL_ROBOT, P.PIP_LISTS[env], P.SCRIPTS / "atest.py"],
        targets=[P.ATEST_OUT / stem / P.ATEST_OUT_XML],
    )


if P.CAN_CONDA_LOCK:

    def task_lock():
        """generate conda lock files for all the excursions"""
        for key, target in P.ENVENTURES.items():
            (flow, pf, py, lab) = key
            file_dep = P.ENV_DEPS[key]
            yield dict(
                name="__".join([p for p in key if p]).replace(".", "_"),
                actions=[[*P.SCRIPT_LOCK, target]],
                file_dep=file_dep,
                targets=[target],
            )


if __name__ == "__main__":
    doit.run(globals())
