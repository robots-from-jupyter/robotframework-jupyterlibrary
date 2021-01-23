import os
import subprocess

from hashlib import sha256

import doit
from doit.tools import PythonInteractiveAction, config_changed, InteractiveAction

from _scripts import project as P
from _scripts.reporter import GithubActionsReporter


os.environ.update(PYTHONIOENCODING="utf-8", MAMBA_NO_BANNER="1")

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
    "reporter": GithubActionsReporter,
}


def task_binder():
    """get to a basic interactive state"""
    return dict(actions=[["echo", "ok"]], file_dep=[P.PIP_LISTS["test"]])


def task_release():
    """the full set of tasks needed for a new release"""
    return dict(
        actions=[["echo", "ok"]],
        file_dep=[
            P.SHA256SUMS,
            P.DOCS_BUILDINFO,
            P.OK.pyflakes,
            P.OK.robot,
            P.OK.prettier,
        ],
    )


def _calc_hash():
    lines = []

    for p in P.HASH_DEPS:
        lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

    output = "\n".join(lines)
    return output


def task_build():
    """build packages"""
    env = "meta"
    env_lock = P.CONDA_LISTS[env]
    run_in = P.RUN_IN[env]

    yield dict(
        name="pypi",
        actions=[[*run_in, *P.PY, "setup.py", "sdist", "bdist_wheel"]],
        targets=[P.SDIST, P.WHEEL],
        file_dep=[*P.PY_SRC, *P.ROBOT_SRC, P.VERSION_FILE, *P.SETUP_CRUFT, env_lock],
    )

    def _update_hash():
        # mimic sha256sum CLI
        if P.SHA256SUMS.exists():
            P.SHA256SUMS.unlink()
        output = _calc_hash()
        print(output)
        P.SHA256SUMS.write_text(output)

    yield dict(
        name="hash",
        file_dep=P.HASH_DEPS,
        targets=[P.SHA256SUMS],
        actions=[_update_hash],
    )


def task_conda_build():
    """build conda package"""

    def _template():
        sums = {
            line.split("  ")[1]: line.split("  ")[0]
            for line in P.SHA256SUMS.read_text().splitlines()
            if line.strip()
        }

        recipe_text = (
            P.META_YAML_IN.read_text()
            .replace("REPLACE_THIS_VERSION", P.VERSION)
            .replace("REPLACE_THIS_PATH", P.SDIST.as_uri())
            .replace("REPLACE_THIS_SHA256", sums[P.SDIST.name])
        )

        print(recipe_text)

        P.META_YAML.write_text(recipe_text)

    if P.CI:
        # we _don't_ want to force irreproducibly re-building the tarball
        file_dep = [P.META_YAML_IN, P.VERSION_FILE]
    else:
        file_dep = [P.META_YAML_IN, P.SDIST, P.VERSION_FILE, P.SHA256SUMS]

    yield dict(
        name="recipe",
        file_dep=file_dep,
        targets=[P.META_YAML],
        actions=[_template],
    )

    yield dict(
        name="build",
        file_dep=[P.META_YAML],
        actions=[
            [
                P.CONDA_EXE,
                "build",
                "-c",
                "conda-forge",
                "--output-folder",
                P.CONDA_BLD,
                P.RECIPE,
            ]
        ],
        targets=[P.CONDA_PKG],
    )


def task_docs():
    """build HTML docs"""
    env = "docs"
    run_in = P.RUN_IN[env]
    lockfile = P.get_lockfile(env)
    frozen = P.PIP_LISTS[env]

    clean, touch = P.get_ok_actions(P.RTD_ENV)

    def _env_from_lock():
        try:
            header, tarballs = lockfile.read_text().split("@EXPLICIT")
        except:
            header = "# NO LOCKFILE"
            tarballs = []

        header = (
            f"# Probably don't edit by hand! \n"
            f"#\n"
            f"# This was generated from {lockfile.relative_to(P.ROOT)}\n"
            f"#\n"
            f"#   doit docs:rtdenv\n"
            f"#\n"
        ) + header

        P.RTD_ENV.write_text(
            header
            + P.safe_dump(
                dict(
                    name="rtd",
                    channels=["conda-forge", "nodefaults"],
                    dependencies=[
                        line.strip() for line in tarballs.strip().splitlines()
                    ],
                )
            )
        )

    yield dict(
        name="rtd:env",
        doc="generate a readthedocs-compatible env",
        file_dep=[lockfile],
        actions=[clean, _env_from_lock],
        targets=[P.RTD_ENV],
    )

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

    clean, touch = P.get_ok_actions(P.OK.black)

    yield dict(
        name="black",
        actions=[clean, [*pym, "black", "--quiet", *P.ALL_PY], touch],
        file_dep=[*P.ALL_PY, env_lock],
        targets=[P.OK.black],
    )

    clean, touch = P.get_ok_actions(P.OK.pyflakes)

    yield dict(
        name="pyflakes",
        actions=[clean, [*pym, "pyflakes", *P.ALL_PY], touch],
        file_dep=[*P.ALL_PY, env_lock, P.OK.black],
        targets=[P.OK.pyflakes],
    )

    clean, touch = P.get_ok_actions(P.OK.robot_tidy)

    yield dict(
        name="robot:tidy",
        actions=[clean]
        + [[*pym, "robot.tidy", "--recursive", it] for it in [P.SRC, P.ATEST]]
        + [touch],
        file_dep=[*P.ALL_ROBOT, env_lock],
        targets=[P.OK.robot_tidy],
    )

    clean, touch = P.get_ok_actions(P.OK.prettier)

    yield dict(
        name="prettier",
        actions=[clean, [*run_in, "yarn", "--silent", "prettier"], touch],
        file_dep=[*P.ALL_PRETTIER, P.YARN_INTEGRITY],
        targets=[P.OK.prettier],
    )


def task_js():
    """javascript cruft"""
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
        doc = f"[{env}] install from dist"
    else:
        pip_args = ["-e", "."]
        doc = f"[{env}] python development install"

    yield dict(
        name=env,
        doc=doc,
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
    """ (dry)run tests"""
    env = "test"
    pym = [*P.RUN_IN[env], *P.PYM]

    dry_run_stem = P.get_atest_stem(
        extra_args=["--dryrun"], lockfile=P.get_lockfile(env), browser=P.BROWSER
    )
    real_stem = P.get_atest_stem(lockfile=P.get_lockfile(env), browser=P.BROWSER)

    dry_target = P.ATEST_OUT / dry_run_stem / P.ATEST_OUT_XML
    real_target = P.ATEST_OUT / real_stem / P.ATEST_OUT_XML

    clean, touch = P.get_ok_actions(P.OK.robot_dry_run)

    robot_deps = [*P.PY_SRC, *P.ALL_ROBOT, P.PIP_LISTS[env], P.SCRIPTS / "atest.py"]

    yield dict(
        name="dryrun",
        uptodate=[config_changed(os.environ.get("ATEST_ARGS", ""))],
        actions=[clean, [*pym, "_scripts.atest", "--dryrun"], touch],
        file_dep=robot_deps,
        targets=[dry_target, P.OK.robot_dry_run],
    )

    clean, touch = P.get_ok_actions(P.OK.robot)

    yield dict(
        name="atest",
        doc="run acceptance tests with robot",
        uptodate=[config_changed(os.environ.get("ATEST_ARGS", ""))],
        actions=[clean, [*pym, "_scripts.atest"], touch],
        file_dep=[P.OK.robot_dry_run, *robot_deps],
        targets=[real_target, P.OK.robot],
    )

    # Presently not running this on CI
    yield dict(
        name="combine",
        doc="combine all robot outputs into a single HTML report",
        actions=[[*pym, "_scripts.combine"]],
        file_dep=[
            real_target,
            *P.ATEST_OUT.rglob(P.ATEST_OUT_XML),
            P.SCRIPTS / "combine.py",
        ],
    )


def _make_lock_task_name(key):
    return "__".join([p for p in key if p]).replace(".", "_")


def _make_lock_task(key, target):
    (flow, pf, py, lab) = key

    task = dict(
        name=_make_lock_task_name(key),
        actions=[[*P.SCRIPT_LOCK, target]],
        file_dep=[*P.ENV_DEPS[key]],
        targets=[target],
    )

    if P.THIS_META_ENV_LOCK != target:
        task["actions"][0] = [*P.RUN_IN["meta"], *task["actions"][0]]
        task["task_dep"] = ["env:meta"]

    return task


# at some point, we'll want a scheduled excursion just for locking
if not (P.CI or P.IN_BINDER):

    def task_lock():
        """generate conda lock files for all the excursions"""
        meta_lock_exists = P.THIS_META_ENV_LOCK.exists()
        can_bootstrap = P.CAN_CONDA_LOCK

        if not (meta_lock_exists or can_bootstrap):
            raise RuntimeError(
                f"{P.THIS_META_ENV_LOCK} is missing: this, or `conda-lock` on path"
                " is needed to bootstrap the lock environment"
            )

        for key, target in P.ENVENTURES.items():
            if not meta_lock_exists and target != P.THIS_META_ENV_LOCK:
                continue

            yield _make_lock_task(key, target)

    def task_publish():
        """publish to pypi"""

        def _check_hash():
            on_disk = P.SHA256SUMS.read_text()
            calculated = _calc_hash()
            print("\n--\n".join(["on-disk:", on_disk, "calculated", calculated]))

            if calculated != on_disk:
                raise RuntimeError("SHA256SUMS do not match:")
            print("SHA256SUMS are OK")

        return dict(
            actions=[
                _check_hash,
                InteractiveAction(
                    [*P.RUN_IN["meta"], "twine", "upload", P.SDIST, P.WHEEL],
                    shell=False,
                ),
            ]
        )


if __name__ == "__main__":
    doit.run(globals())
