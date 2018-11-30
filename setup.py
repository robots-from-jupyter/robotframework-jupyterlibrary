import os
import re

from setuptools import setup


HERE = os.path.dirname(__file__)

with open(os.path.join(HERE, "src", "JupyterLibrary", "_version.py")) as fp:
    version = re.findall(r"""__version__ = "([^"]+)""", fp.read())[0]

setup(version=version)
