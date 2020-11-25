import os
import platform
from os.path import abspath, dirname, join

HERE = dirname(__file__)
ROOT = abspath(join(HERE, ".."))
TESTS = abspath(join(ROOT, "atest", "acceptance"))

TEST_OUT = abspath(join(ROOT, "build", "test_output"))

PLATFORM = platform.system().lower()
BROWSER = os.environ.get("BROWSER", "headlessfirefox")
