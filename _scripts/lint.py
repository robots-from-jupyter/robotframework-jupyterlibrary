"""Apply source normalization and checking.

This should run without JupyterLibrary installed, but only needs to
work on Python3
"""
from pathlib import Path
from subprocess import check_call

from nbformat import NO_CONVERT, read, write

PY_SRC = ["src", "setup.py", "scripts", "docs"]
RF_SRC = ["atest", "src"]


def lint():
    check_call(["isort", "-rc", *PY_SRC])
    check_call(["black", *PY_SRC])
    check_call(["flake8", *PY_SRC])

    for src in RF_SRC:
        check_call(["robotidy", "-r", src])

    for nbp in (Path(__file__).parent.parent / "docs").rglob("*.ipynb"):
        nbf = read(str(nbp), NO_CONVERT)
        changed = False
        for cell in nbf.cells:
            if cell.cell_type == "code":
                if cell.outputs:
                    cell.outputs = []
                    changed = True
                if cell.execution_count:
                    cell.execution_count = None
                    changed = True
        if changed:
            print(f"Overwriting {nbp}")
            write(nbf, str(nbp))


if __name__ == "__main__":
    lint()
