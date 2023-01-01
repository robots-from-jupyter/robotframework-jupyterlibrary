import os
import shutil
import socket
import tempfile
import typing
import time
import subprocess
from os.path import join
from uuid import uuid4

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword
from urllib.request import urlopen


class ServerKeywords(LibraryComponent):
    _handles = []
    _tmpdirs = {}
    _notebook_dirs = {}
    _ports = {}
    _base_urls = {}
    _tokens = {}

    _app_name = None

    @keyword
    def set_default_jupyter_app_name(
        self, app_name: typing.Optional[str] = None
    ) -> typing.Optional[str]:
        """Set the current ``traitlets.Configurable`` Jupyter Server application,
        returning the previous value.

        A value of ``None`` (the default) will try to detect the app based on
        command name, such as:

        - ``jupyter-notebook`` is configured with ``NotebookApp``
        - ``jupyter-lab`` and most other are configured with ``ServerApp``

        This may also be set externally via the ``JUPYTER_LIBRARY_APP`` environment
        variable, but any explicit argument will override this.

        See [#Get Jupyter App Name] for more.
        """
        old_app_name = self.app_name
        self.app_name = app_name
        return old_app_name

    @keyword
    def get_jupyter_app_name(
        self, command: typing.Optional[str] = None
    ) -> typing.Optional[str]:
        """Get the current ``traitlets.Configurable`` Jupyter Server application,
        optionally for a specific CLI command.

        See [#Set Default Jupyter App Name] for more.
        """
        app_name = os.environ.get("JUPYTER_LIBRARY_APP")

        if self._app_name is not None:
            app_name = self._app_name
        elif command is not None and "jupyter-notebook" in command:
            app_name = "NotebookApp"

        return app_name or "ServerApp"

    @keyword
    def start_new_jupyter_server(
        self,
        command: typing.Optional[str] = "jupyter-notebook",
        port: typing.Optional[int] = None,
        base_url: typing.Optional[str] = "/@rf/",
        notebook_dir: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        *args,
        **config,
    ) -> subprocess.Popen:
        """Start a Jupyter server. All arguments are optional.

        | = argument =     | = default =           | = notes =                          |
        | ``command``      | ``jupyter-notebook``  | e.g. ``jupyter-lab``               |
        | ``port``         | an unused port        |                                    |
        | ``base_url``     | ``/@rf/``             |                                    |
        | ``notebook_dir`` | a temporary directory |                                    |
        | ``token``        | a random ``uuid4``    |                                    |
        | ``*args``        |                       | extra server arguments             |
        | ``**config``     |                       | extra process arguments            |
        | ``app_name``     | ``None`` (detect)     | e.g. ``NotebookApp``, `ServerApp`` |

        If not configured, the ``%{HOME}`` environment variable and current
        working directory will be set to avoid leaking configuration
        between between runs (or the test instance) itself. These
        directories will be cleaned up after the server process is
        [#Terminate All Jupyter Servers|terminated].

        The ``app_name`` argument is as described for the [#Get Jupyter App Name|app name],
        with the default being to autodetect from the command and environment.
        """
        app_name = (
            config.pop("app_name", None)
            or config.get("env:JUPYTER_LIBRARY_APP")
            or self.get_jupyter_app_name(command)
        )
        port = port or self.get_unused_port()
        token = str(uuid4()) if token is None else token

        BuiltIn().import_library("Process")
        plib = BuiltIn().get_library_instance("Process")

        tmpdir = tempfile.mkdtemp()

        if "env:HOME" not in config:
            home_dir = join(tmpdir, "home")
            os.mkdir(home_dir)
            config["env:HOME"] = home_dir

        if "stdout" not in config:
            config["stdout"] = join(tmpdir, "server.log")

        if "stderr" not in config:
            config["stderr"] = "STDOUT"

        if notebook_dir is None:
            notebook_dir = join(tmpdir, "notebooks")
            os.mkdir(notebook_dir)
            config["cwd"] = notebook_dir

        args = args or self.build_jupyter_server_arguments(
            port, base_url, token, app_name
        )

        handle = plib.start_process(command, *args, **config)

        self._handles += [handle]
        self._tmpdirs[handle] = tmpdir
        self._notebook_dirs[handle] = notebook_dir
        self._ports[handle] = port
        self._base_urls[handle] = base_url
        self._tokens[handle] = token

        return handle

    @keyword
    def build_jupyter_server_arguments(
        self,
        port: int,
        base_url: str,
        token: str,
        app_name: typing.Optional[str] = None,
    ) -> typing.List[str]:
        """Build Some default Jupyter application arguments.

        If the ``app_name`` is not provided, it will be detected based on the rules
        in [#Get Jupyter App Name]."""
        app_name = app_name or self.get_jupyter_app_name()
        return [
            "--no-browser",
            "--debug",
            f"--port={port}",
            f"--{app_name}.token={token}",
            f"--{app_name}.base_url={base_url}",
        ]

    @keyword
    def copy_files_to_jupyter_directory(self, *sources: str, **kwargs) -> None:
        """Copy some files into the (temporary) jupyter server root.

        | = argument = | = default =                       |
        | ``nbserver`` | the most-recently launched server |
        """
        nbserver = kwargs.get("nbserver", self._handles[-1])
        notebook_dir = self._notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        return osli.copy_files(*(list(sources) + [notebook_dir]))

    @keyword
    def copy_files_from_jupyter_directory(self, *src_and_dest: str, **kwargs) -> None:
        """Copy some files from the (temporary) jupyter server root

        | = argument = | = default =                       |
        | ``nbserver`` | the most-recently launched server |

        Patterns will have the notebook directory prepended
        """
        nbserver = kwargs.get("nbserver", self._handles[-1])
        notebook_dir = self._notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        sources = [join(notebook_dir, src) for src in src_and_dest[:-1]]
        dest = src_and_dest[-1]
        return osli.copy_files(*sources + [dest])

    @keyword
    def get_jupyter_directory(
        self, nbserver: typing.Optional[subprocess.Popen] = None
    ) -> str:
        """
        | = argument = | = default =                       |
        | ``nbserver`` | the most-recently launched server |
        """
        nbserver = nbserver if nbserver is not None else self._handles[-1]
        return self._notebook_dirs[nbserver]

    @keyword
    def wait_for_jupyter_server_to_be_ready(
        self, *nbservers: subprocess.Popen, **kwargs
    ) -> int:
        """Wait for the most-recently started Jupyter server to be ready"""
        interval = float(kwargs.get("interval", 0.5))
        retries = int(kwargs.get("retries", 60))

        if not nbservers:
            if not self._handles:
                return 0
            nbservers = [self._handles[-1]]

        ready = 0
        error = None

        while retries and ready != len(nbservers):
            retries -= 1
            ready = 0
            try:
                for nbh in nbservers:
                    urlopen(self.get_jupyter_server_url(nbh))
                    ready += 1
            except Exception as _error:
                time.sleep(interval)
                error = _error

        assert ready == len(nbservers), (
            f"Only {ready} of {len(nbservers)} servers were ready after "
            f"{interval * retries}s. Last error: {type(error)} {error}"
        )
        return ready

    @keyword
    def get_jupyter_server_url(
        self, nbserver: typing.Optional[subprocess.Popen] = None
    ) -> str:
        """Get the given (or most recently-launched) server's URL"""
        nbh = nbserver or self._handles[-1]
        return f"http://127.0.0.1:{self._ports[nbh]}{self._base_urls[nbh]}"

    @keyword
    def get_jupyter_server_token(
        self, nbserver: typing.Optional[subprocess.Popen] = None
    ) -> str:
        """Get the given (or most recently-launched) server's token"""
        nbh = nbserver or self._handles[-1]
        return self._tokens[nbh]

    @keyword
    def wait_for_new_jupyter_server_to_be_ready(
        self, command: typing.Optional[str] = None, *args, **config
    ) -> subprocess.Popen:
        """Get the given (or most recently-launched) server's token. See
        [#Start New Jupyter Server|Start New Jupyter Server]
        """
        handle = self.start_new_jupyter_server(command, *args, **config)
        self.wait_for_jupyter_server_to_be_ready(handle)
        return handle

    @keyword
    def terminate_all_jupyter_servers(self, timeout: str = "6s") -> int:
        """Close all Jupyter servers started by
        [#Start New Jupyter Server|Start New Jupyter Server],
        waiting ``timeout`` to ensure all files/processes are freed before
        cleaning up temporary directories, if any.
        """
        plib = BuiltIn().get_library_instance("Process")

        self.wait_for_jupyter_server_to_be_ready()

        terminated = 0
        shutdown = 0
        for nbh in self._handles:
            url = self.get_jupyter_server_url(nbh)
            token = self.get_jupyter_server_token(nbh)
            try:
                urlopen(f"{url}api/shutdown?token={token}", data=[])
                shutdown += 1
            except Exception as err:
                BuiltIn().log(err)

        if shutdown:
            for nbh in self._handles:
                try:
                    plib.terminate_process(nbh)
                    terminated += 1
                except Exception as err:
                    BuiltIn().log(err)
            if self._handles:
                BuiltIn().sleep(timeout)
            for nbh in self._handles:
                try:
                    plib.terminate_process(nbh, kill=True)
                except Exception as err:
                    BuiltIn().log(err)

        # give processes a mo to shutdown
        if terminated or shutdown and self._tmpdirs:
            for nbh in self._handles:
                shutil.rmtree(self._tmpdirs[nbh])

        self._handles = []
        self._tmpdirs = {}
        self._notebook_dirs = {}
        self._ports = {}
        self._base_urls = {}
        self._tokens = {}

        return terminated

    @keyword
    def get_unused_port(self) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
