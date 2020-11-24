from _scripts import project as P
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    "default_tasks": ["binder"],
}

def task_binder():
    """get to a basic interactive state"""
    return dict(
        actions=[["echo", "ok"]]
    )

def task_build():
    yield dict(
        name="pypi",
        actions=[[*P.PY, "setup.py", "sdist", "bdist_wheel"]]
    )

def task_lock():
    """ generate conda lock files for all the excursions
    """
    for (flow, pf, py, lab), target in P.ENVENTURES.items():
        file_dep = P.ENV_DEPS[flow, pf, py, lab]
        yield dict(
            name=f"{flow}_{pf}__py{py}__lab{lab}".replace(".", "_"),
            actions=[
                [*P.SCRIPT_LOCK, target]
            ],
            file_dep=file_dep,
            targets=[target]
        )
