from SeleniumLibrary import SeleniumLibrary

from .keywords import (
    server,
)


class JupyterLibrary(SeleniumLibrary):
    """JupyterLibrary is a Jupyter testing library for Robot Framework."""
    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None):
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
            screenshot_root_directory=None
        )
        self.add_library_components([
            server
        ])
