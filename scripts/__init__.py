import os
import platform
from os.path import abspath, dirname, join

HERE = dirname(__file__)
TESTS = abspath(join(HERE, "..", "atest", "acceptance"))

TEST_OUT = abspath(join(HERE, "..", "_artifacts", "test_output"))

PLATFORM = platform.system().lower()
BROWSER = os.environ.get("BROWSER", "headlessfirefox")
