from .core import JupyterLibrary
from pathlib import Path

__version__ = (Path(__file__).parent / "VERSION").read_text()

__all__ = ["__version__", "JupyterLibrary"]
