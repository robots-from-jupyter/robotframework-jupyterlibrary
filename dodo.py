"""Project automation for ``robotframework-jupyterlibrary``."""
import os
import subprocess
from hashlib import sha256

import doit
from doit.tools import InteractiveAction, PythonInteractiveAction, config_changed
from yaml import safe_dump

from _scripts import project as P
from _scripts.reporter import GithubActionsReporter

os.environ.update(
    PYTHONIOENCODING="utf-8",
    MAMBA_NO_BANNER="1",
    PYDEVD_DISABLE_FILE_VALIDATION="1",
)

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
    "reporter": GithubActionsReporter,
}


def task_binder():
    """Get to a basic interactive state."""
    return {"actions": [["echo", "ok"]], "file_dep": [P.PIP_LISTS["test"]]}


def task_release():
    """Run the full set of tasks needed for a new release."""
    return {
        "actions": [["echo", "ok"]],
        "file_dep": [
            P.SHA256SUMS,
            P.DOCS_BUILDINFO,
            P.OK.ruff,
            P.OK.robot,
            P.OK.prettier,
        ],
    }


def _calc_hash():
    lines = []

    for p in P.HASH_DEPS:
        lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

    output = "\n".join(lines)
    return output


def task_build():
    """Build packages."""
    env = "meta"
    env_lock = P.CONDA_LISTS[env]
    run_in = P.RUN_IN[env]

    def _flit_build():
        env = dict(os.environ, SOURCE_DATE_EPOCH=P.get_source_date_epoch())
        rc = subprocess.call([*run_in, "flit", "--debug", "build"], env=env)
        return rc == 0

    yield {
        "name": "pypi",
        "doc": "build the pypi sdist/wheel",
        "actions": [_flit_build],
        "targets": [P.SDIST, P.WHEEL],
        "file_dep": [*P.PY_SRC, *P.ROBOT_SRC, *P.SETUP_CRUFT, env_lock],
    }

    def _update_hash():
        # mimic sha256sum CLI
        if P.SHA256SUMS.exists():
            P.SHA256SUMS.unlink()
        output = _calc_hash()
        print(output)
        P.SHA256SUMS.write_text(output)

    yield {
        "name": "hash",
        "doc": "generate a hash file of all distributions",
        "file_dep": P.HASH_DEPS,
        "targets": [P.SHA256SUMS],
        "actions": [_update_hash],
    }


def task_conda_build():
    """Build conda package."""

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
        file_dep = [P.META_YAML_IN, P.PPT]
    else:
        file_dep = [P.META_YAML_IN, P.SDIST, P.PPT, P.SHA256SUMS]

    yield {
        "name": "recipe",
        "doc": "update the conda recipe",
        "file_dep": file_dep,
        "targets": [P.META_YAML],
        "actions": [_template],
    }

    yield {
        "name": "build",
        "doc": "use boa to build the conda package",
        "file_dep": [P.META_YAML],
        "actions": [
            [
                P.CONDA_EXE,
                "mambabuild",
                "-c",
                "conda-forge",
                "--output-folder",
                P.CONDA_BLD,
                P.RECIPE,
            ],
        ],
        "targets": [P.CONDA_PKG],
    }


def task_docs():
    """Build HTML docs."""
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
            f"#   doit docs:rtd:env\n"
            f"#\n"
        ) + header

        P.RTD_ENV.write_text(
            header
            + safe_dump(
                {
                    "name": "rtd",
                    "channels": ["conda-forge", "nodefaults"],
                    "dependencies": [
                        line.strip() for line in tarballs.strip().splitlines()
                    ],
                },
            ),
        )

    yield {
        "name": "rtd:env",
        "doc": "generate a readthedocs-compatible env",
        "file_dep": [lockfile],
        "actions": [clean, _env_from_lock],
        "targets": [P.RTD_ENV],
    }

    yield {
        "name": "sphinx",
        "doc": "build the docs with sphinx",
        "actions": [
            [
                *run_in,
                "sphinx-build",
                "-W",
                "-a",
                "-b",
                "html",
                "docs",
                "build/docs/html",
            ],
        ],
        "file_dep": [frozen, *P.ALL_DOCS_SRC, *P.SETUP_CRUFT, *P.ROBOT_SRC, P.DODO],
        "targets": [P.DOCS_BUILDINFO],
    }


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
                    [P.CONDA_EXE, "list", "--explicit", "--md5", *env_args],
                ),
            ),
            None,
        ][-1],
    ]

    yield {
        "name": env,
        "doc": f"create the local {env} environment",
        "file_dep": [lockfile],
        "actions": actions,
        "targets": [explicit_list],
    }


def task_env():
    """Prepare envs."""
    for env in P.ENV_NAMES:
        task = _make_env(env)
        if task:
            yield task


def task_lint():
    """Lint code."""
    env = "lint"
    env_lock = P.CONDA_LISTS["lint"]
    run_in = P.RUN_IN[env]
    pym = [*run_in, *P.PYM]

    clean, touch = P.get_ok_actions(P.OK.ssort)

    yield {
        "name": "ssort",
        "doc": "apply source ordering to python",
        "actions": [clean, [*pym, "ssort", *P.ALL_PY], touch],
        "file_dep": [*P.ALL_PY, env_lock],
        "targets": [P.OK.ssort],
    }

    clean, touch = P.get_ok_actions(P.OK.black)

    yield {
        "name": "black",
        "doc": "ensure python code is well-formatted",
        "actions": [clean, [*pym, "black", "--quiet", *P.ALL_PY], touch],
        "file_dep": [*P.ALL_PY, env_lock, P.OK.ssort],
        "targets": [P.OK.black],
    }

    clean, touch = P.get_ok_actions(P.OK.ruff)

    yield {
        "name": "ruff",
        "doc": "ensure python code is well-behaved",
        "actions": [clean, [*pym, "ruff", "--fix", *P.ALL_PY], touch],
        "file_dep": [*P.ALL_PY, env_lock, P.OK.black, P.PPT],
        "targets": [P.OK.ruff],
    }

    clean, touch = P.get_ok_actions(P.OK.robotidy)

    yield {
        "name": "robotidy",
        "doc": "ensure robot code is well-formatted",
        "actions": [clean, [*run_in, *P.ROBOTIDY_ARGS, P.SRC, P.ATEST], touch],
        "file_dep": [*P.ALL_ROBOT, env_lock],
        "targets": [P.OK.robotidy],
    }

    clean, touch = P.get_ok_actions(P.OK.robocop)

    yield {
        "name": "robocop",
        "doc": "ensure robot code is well-behaved",
        "actions": [clean, [*run_in, *P.ROBOCOP_ARGS, P.SRC, P.ATEST], touch],
        "file_dep": [*P.ALL_ROBOT, env_lock, P.OK.robotidy],
        "targets": [P.OK.robocop],
    }

    clean, touch = P.get_ok_actions(P.OK.prettier)

    yield {
        "name": "prettier",
        "doc": "ensure markdown, YAML, JSON, etc. are well-formatted",
        "actions": [clean, [*run_in, "yarn", "--silent", "prettier"], touch],
        "file_dep": [*P.ALL_PRETTIER, P.YARN_INTEGRITY],
        "targets": [P.OK.prettier],
    }


def task_js():
    """Javascript cruft."""
    env = "lint"

    run_in = P.RUN_IN[env]
    env_lock = P.CONDA_LISTS[env]

    yield {
        "name": "yarn",
        "doc": "install nodejs dev dependencies",
        "uptodate": [
            config_changed({k: P.PACKAGE[k] for k in ["devDependencies", "prettier"]}),
        ],
        "file_dep": [P.YARN_LOCK, env_lock],
        "actions": [
            [*run_in, "yarn", "--silent", "--prefer-offline", "--ignore-optional"],
        ],
        "targets": [P.YARN_INTEGRITY],
    }


def task_lab():
    """Start a jupyter lab server (with all other extensions)."""
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
        yield {
            "name": "ext",
            "uptodate": [config_changed({"labextensions": P.LAB_EXTENSIONS})],
            "actions": [
                [*lab_ext, "install", *app_dir, *P.LAB_EXTENSIONS, "--no-build"],
                [*lab, "build", *app_dir, "--debug"],
            ],
            "file_dep": [frozen],
            "targets": [P.APP_INDEX],
        }
        serve_deps += [P.APP_INDEX]

    def _lab():
        p = subprocess.Popen(
            [*lab, *app_dir, "--no-browser", "--debug"],
            stdin=subprocess.PIPE,
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

    yield {
        "name": "serve",
        "doc": "runs lab (never stops)",
        "uptodate": [lambda: False],
        "actions": [PythonInteractiveAction(_lab)],
        "file_dep": serve_deps,
    }


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
            P.PPT_DATA["project"]["name"],
        ]
        doc = f"[{env}] install from dist"
    else:
        pip_args = ["-e", ".", "--no-deps", "--no-build-isolation"]
        doc = f"[{env}] python development install"

    yield {
        "name": env,
        "doc": doc,
        "actions": [
            lambda: frozen.unlink() if frozen.exists() else None,
            [
                *pym,
                "pip",
                "install",
                "--no-deps",
                "--ignore-installed",
                "--no-build-isolation",
                *pip_args,
            ],
            [*pym, "pip", "check"],
            lambda: [
                frozen.write_bytes(subprocess.check_output([*pym, "pip", "freeze"])),
                None,
            ][-1],
        ],
        "targets": [frozen],
        "file_dep": file_dep,
    }


def task_setup():
    """Do an editable install of the package."""
    for env in P.ENV_NAMES:
        if env == "meta":
            continue
        yield _make_setup(env)


def task_test():
    """(dry)run tests."""
    env = "test"
    pym = [*P.RUN_IN[env], *P.PYM]

    dry_run_stem = P.get_atest_stem(
        extra_args=["--dryrun"],
        lockfile=P.get_lockfile(env),
        browser=P.BROWSER,
    )
    real_stem = P.get_atest_stem(lockfile=P.get_lockfile(env), browser=P.BROWSER)

    dry_target = P.ATEST_OUT / dry_run_stem / P.ATEST_OUT_XML
    real_target = P.ATEST_OUT / real_stem / P.ATEST_OUT_XML

    clean, touch = P.get_ok_actions(P.OK.robot_dry_run)

    robot_deps = [*P.PY_SRC, *P.ALL_ROBOT, P.PIP_LISTS[env], P.SCRIPTS / "atest.py"]

    yield {
        "name": "dryrun",
        "doc": "pass the tests through the robot machinery, but don't actually _run_ anything",
        "uptodate": [config_changed(os.environ.get("ATEST_ARGS", ""))],
        "actions": [clean, [*pym, "_scripts.atest", "--dryrun"], touch],
        "file_dep": robot_deps,
        "targets": [dry_target, P.OK.robot_dry_run],
    }

    clean, touch = P.get_ok_actions(P.OK.robot)

    yield {
        "name": "atest",
        "doc": "run acceptance tests with robot",
        "uptodate": [config_changed(os.environ.get("ATEST_ARGS", ""))],
        "actions": [clean, [*pym, "_scripts.atest"], touch],
        "file_dep": [P.OK.robot_dry_run, *robot_deps],
        "targets": [real_target, P.OK.robot],
    }


@doit.create_after("test:atest")
def task_report():
    """Generate reports of test data."""
    env = "test"
    pym = [*P.RUN_IN[env], *P.PYM]

    cov_cmd = [*pym, "coverage"]
    cov_data = [f"--data-file={P.ATEST_COV}"]
    all_cov = sorted(P.ATEST_OUT.rglob("coverage/.coverage*"))
    real_stem = P.get_atest_stem(lockfile=P.get_lockfile(env), browser=P.BROWSER)
    real_target = P.ATEST_OUT / real_stem / P.ATEST_OUT_XML

    yield {
        "name": "cov:combine",
        "doc": "gather coverage",
        "task_dep": ["test:atest"],
        "targets": [P.ATEST_COV],
        "file_dep": [*all_cov],
        "actions": [[*cov_cmd, "combine", *cov_data, "--keep", *all_cov]],
    }

    yield {
        "name": "cov:html:rfsl",
        "doc": "generate coverage html",
        "file_dep": [P.ATEST_COV],
        "targets": [P.ATEST_HTMLCOV_RFSL_INDEX],
        "actions": [
            [
                *cov_cmd,
                "html",
                "--show-contexts",
                "--include=*/SeleniumLibrary/*",
                *cov_data,
                f"--directory={P.ATEST_HTMLCOV_RFSL}",
            ],
        ],
    }

    yield {
        "name": "cov:html:se",
        "doc": "generate coverage html",
        "file_dep": [P.ATEST_COV],
        "targets": [P.ATEST_HTMLCOV_SE_INDEX],
        "actions": [
            [
                *cov_cmd,
                "html",
                "--show-contexts",
                "--include=*/selenium/*",
                *cov_data,
                f"--directory={P.ATEST_HTMLCOV_SE}",
            ],
        ],
    }

    yield {
        "name": "cov:html:rfjl",
        "doc": "generate coverage html",
        "file_dep": [P.ATEST_COV],
        "targets": [P.ATEST_HTMLCOV_RFJL_INDEX],
        "actions": [
            [
                *cov_cmd,
                "html",
                "--show-contexts",
                "--include=*/JupyterLibrary/*",
                *cov_data,
                f"--directory={P.ATEST_HTMLCOV_RFJL}",
            ],
        ],
    }

    yield {
        "name": "cov:report",
        "doc": "emit coverage console report and check",
        "file_dep": [P.ATEST_COV, P.ATEST_HTMLCOV_RFJL_INDEX],
        "actions": [
            [
                *cov_cmd,
                "report",
                *cov_data,
                "--show-missing",
                "--skip-covered",
                "--include=*/JupyterLibrary/*",
                f"--fail-under={P.COV_FAIL_UNDER_RFJL}",
            ],
        ],
    }

    yield {
        "name": "robot:combine",
        "doc": "combine all robot outputs into a single HTML report",
        "actions": [[*pym, "_scripts.combine"]],
        "file_dep": [real_target, P.SCRIPTS / "combine.py"],
    }


def _make_lock_task_name(key):
    return "__".join([p for p in key if p]).replace(".", "_")


def _make_lock_task(key, target):
    (flow, pf, py, lab) = key

    ft = [k for k in [py, lab] if k]
    if ft:
        ft = f"(ft. {', '.join(ft)})"

    task = {
        "name": _make_lock_task_name(key),
        "doc": f"lock the {flow} environment for {pf} {ft}".strip(),
        "actions": [[*P.SCRIPT_LOCK, target]],
        "file_dep": [*P.ENV_DEPS[key]],
        "targets": [target],
    }

    if target != P.THIS_META_ENV_LOCK:
        task["actions"][0] = [*P.RUN_IN["meta"], *task["actions"][0]]
        task["task_dep"] = ["env:meta"]

    return task


# at some point, we'll want a scheduled excursion just for locking
if not (P.CI or P.IN_BINDER):

    def task_lock():
        """Generate conda lock files for all the excursions."""
        meta_lock_exists = P.THIS_META_ENV_LOCK.exists()
        can_bootstrap = P.CAN_CONDA_LOCK

        if not (meta_lock_exists or can_bootstrap):
            msg = f"{P.THIS_META_ENV_LOCK} is missing: this, or `conda-lock` on path is needed to bootstrap the lock environment"
            raise RuntimeError(
                msg,
            )

        for key, target in P.ENVENTURES.items():
            if not meta_lock_exists and target != P.THIS_META_ENV_LOCK:
                continue

            yield _make_lock_task(key, target)

    def task_publish():
        """Publish distributioons."""

        def _check_hash():
            on_disk = P.SHA256SUMS.read_text()
            calculated = _calc_hash()
            print("\n--\n".join(["on-disk:", on_disk, "calculated", calculated]))

            if calculated != on_disk:
                msg = "SHA256SUMS do not match:"
                raise RuntimeError(msg)
            print("SHA256SUMS are OK")

        yield {
            "name": "pypi",
            "doc": "upload python sdist and wheel to PyPI",
            "actions": [
                _check_hash,
                InteractiveAction(
                    [*P.RUN_IN["meta"], "twine", "upload", P.SDIST, P.WHEEL],
                    shell=False,
                ),
            ],
        }


if __name__ == "__main__":
    doit.run(globals())
