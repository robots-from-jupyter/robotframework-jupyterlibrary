""" Core library entrypoint for JupyterLibrary

    We <3 Python3, but for the time being, this module should also run in Python2
"""
from glob import glob
from os.path import basename, dirname, isdir, join

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.utils.librarylistener import LibraryListener

from .keywords import server


CLIENTS = [
    client for client in glob(join(dirname(__file__), "clients", "*")) if isdir(client)
]

COMMON = list(glob(join(dirname(__file__), "common", "*.robot")))

component_classes = [server.ServerKeywords]


class JupyterLibrary(SeleniumLibrary):
    """JupyterLibrary is a Jupyter testing library for Robot Framework."""

    def __init__(
        self,
        timeout=5.0,
        implicit_wait=0.0,
        run_on_failure="Capture Page Screenshot",
        screenshot_root_directory=None,
    ):
        """JupyterLibrary can be imported with several optional arguments.
        - ``timeout``:
          Default value for `timeouts` used with ``Wait ...`` keywords.
        - ``implicit_wait``:
          Default value for `implicit wait` used when locating elements.
        - ``run_on_failure``:
          Default action for the `run-on-failure functionality`.
        - ``screenshot_root_directory``:
          Location where possible screenshots are created. If not given,
          the directory where the log file is written is used.
        """
        super(JupyterLibrary, self).__init__(
            timeout=5.0,
            implicit_wait=0.0,
            run_on_failure="Capture Page Screenshot",
            screenshot_root_directory=None,
        )
        self.add_library_components(
            [Component(self) for Component in component_classes]
        )
        self.ROBOT_LIBRARY_LISTENER = JupyterLibraryListener()


class JupyterLibraryListener(LibraryListener):
    """Custom listener to do per-suite imports of resource files"""

    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attrs):
        super(JupyterLibraryListener, self).start_suite(name, attrs)
        resources = []

        for common in COMMON:
            resources += ["JupyterLibrary/common/{}".format(basename(common))]

        for client in CLIENTS:
            for path in glob(join(client, "*.robot")):
                resources += [
                    "JupyterLibrary/clients/{}/{}".format(
                        basename(client), basename(path)
                    )
                ]

        for resource in resources:
            BuiltIn().import_resource(resource)
