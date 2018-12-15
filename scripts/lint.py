from pathlib import Path
from subprocess import check_call

from nbformat import NO_CONVERT, read, write


PY_SRC = ["src", "setup.py", "scripts", "docs"]
RF_SRC = ["atest", "src"]


def lint():
    check_call(["isort", "-rc"] + PY_SRC)
    check_call(["black"] + PY_SRC)
    check_call(["flake8"] + PY_SRC)

    for src in RF_SRC:
        check_call(["python", "-m", "robot.tidy", "-r", src])

    for nbp in (Path(__file__).parent / "docs").rglob("*.ipynb"):
        nbf = read(nbp, NO_CONVERT)
        changed = False
        for cell in nbf:
            if cell.cell_type == "code_cell":
                if cell.outputs:
                    cell.outputs = []
                    changed = True
                if cell.execution_count:
                    cell.execution_count = None
                    changed = True
        if changed:
            write(nbf, nbp)


if __name__ == "__main__":
    lint()
