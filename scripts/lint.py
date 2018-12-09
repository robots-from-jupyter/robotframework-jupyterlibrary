from subprocess import check_call


PY_SRC = ["src", "setup.py", "scripts", "docs"]
RF_SRC = ["atest", "src"]


def lint():
    check_call(["isort", "-rc"] + PY_SRC)
    check_call(["black"] + PY_SRC)
    check_call(["flake8"] + PY_SRC)

    for src in RF_SRC:
        check_call(["python", "-m", "robot.tidy", "-r", src])


if __name__ == "__main__":
    lint()
