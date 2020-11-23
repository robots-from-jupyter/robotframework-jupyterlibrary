from _scripts import project as P

def task_lock():
    """ generate lock files for all the excursions
    """
    for (pf, py, lab), target in P.ENVENTURES.items():
        yield dict(
            name=f"{pf}__py{py}__lab{lab}".replace(".", "_"),
            actions=[
                ["python", "-m", "_scripts.lock", pf, py, lab]
            ],
            file_dep=P.ENV_DEPS[pf, py, lab],
            targets=[target]
        )
