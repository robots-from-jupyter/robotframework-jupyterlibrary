"""A Robot Framework library for automating (testing of) Jupyter end-user applications and extensions."""
from pathlib import Path

from .core import JupyterLibrary

__version__ = (Path(__file__).parent / "VERSION").read_text()

__all__ = ["__version__", "JupyterLibrary", "load_ipython_extension"]


def load_ipython_extension(ip):
    """Register the ``%robot`` magic."""
    from .magic import RobotMagics

    ip.register_magics(RobotMagics)
