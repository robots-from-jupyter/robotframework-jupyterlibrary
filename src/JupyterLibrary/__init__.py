"""A Robot Framework library for automating (testing of) Jupyter end-user applications and extensions."""
from ._version import __version__
from .core import JupyterLibrary

__all__ = ["__version__", "JupyterLibrary", "load_ipython_extension"]


def load_ipython_extension(ip):
    """Register the ``%robot`` magic."""
    from .magic import RobotMagics

    ip.register_magics(RobotMagics)
