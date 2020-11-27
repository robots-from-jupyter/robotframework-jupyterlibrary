from pathlib import Path

from .core import JupyterLibrary
from .magic import load_ipython_extension

__version__ = (Path(__file__).parent / "VERSION").read_text()

__all__ = ["__version__", "JupyterLibrary", "load_ipython_extension"]
