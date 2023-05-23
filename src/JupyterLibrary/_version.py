from .constants import NAME

__all__ = ["__version__"]

__version__: str = __import__("importlib.metadata").metadata.version(NAME)
