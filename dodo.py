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


def task_lock():
    """ generate conda lock files for all the excursions
    """
    for (pf, py, lab), target in P.ENVENTURES.items():
        yield dict(
            name=f"{pf}__py{py}__lab{lab}".replace(".", "_"),
            actions=[
                [*P.SCRIPT_LOCK, "--platform", pf, "--python", py, "--lab", lab]
            ],
            file_dep=P.ENV_DEPS[pf, py, lab],
            targets=[target]
        )
