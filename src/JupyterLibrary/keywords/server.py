"""A library component for managing Jupyter servers."""
import os
import shutil
import socket
import subprocess
import tempfile
import time
import typing
from pathlib import Path
from urllib.request import urlopen
from uuid import uuid4

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword


class ServerKeywords(LibraryComponent):

    """A component that extends the core with Jupyter server management."""

    _handles: typing.List[subprocess.Popen]
    _tmpdirs: typing.Dict[subprocess.Popen, str]
    _notebook_dirs: typing.Dict[subprocess.Popen, str]
    _ports: typing.Dict[subprocess.Popen, int]
    _base_urls: typing.Dict[subprocess.Popen, str]
    _tokens: typing.Dict[subprocess.Popen, str]
    _app_name: typing.Optional[str]

    def __init__(self, *args, **kwargs):
        """Initialize a library with jupyter server keywords."""
        super().__init__(*args, **kwargs)
        self._handles = []
        self._tmpdirs = {}
        self._notebook_dirs = {}
        self._ports = {}
        self._base_urls = {}
        self._tokens = {}
        self._app_name = None

    @keyword
    def set_default_jupyter_app_name(
        self,
        app_name: typing.Optional[str] = None,
    ) -> typing.Optional[str]:
        """Set the current ``traitlets.Configurable`` Jupyter Server application, returning the previous value.

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
        self,
        command: typing.Optional[str] = None,
    ) -> typing.Optional[str]:
        """Get the current ``traitlets.Configurable`` Jupyter Server application, optionally for a specific CLI command.

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

        | = argument =     | = default =           | = notes =                               |
        | ``command``      | ``jupyter-notebook``  | e.g. ``jupyter-lab``                    |
        | ``port``         | an unused port        |                                         |
        | ``base_url``     | ``/@rf/``             |                                         |
        | ``notebook_dir`` | a temporary directory |                                         |
        | ``token``        | a random ``uuid4``    |                                         |
        | ``*args``        |                       | extra server arguments                  |
        | ``**config``     |                       | extra process arguments                 |
        | ``app_name``     | ``None`` (detect)     | e.g. ``NotebookApp``, `ServerApp``      |
        | ``extra_args``   | ``[]``                | extra arguments beyond ```token``, etc. |

        If not configured, the ``%{HOME}`` environment variable and current
        working directory will be set to avoid leaking configuration
        between between runs (or the test instance) itself. These
        directories will be cleaned up after the server process is
        [#Terminate All Jupyter Servers|terminated].

        The ``app_name`` argument is as described for the [#Get Jupyter App Name|app name],
        with the default being to autodetect from the command and environment.

        ``extra_args`` are passed to ``Start Process`` before the ``token``
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

        tmp_path = Path(tempfile.mkdtemp())

        if "env:HOME" not in config:
            home_dir = tmp_path / "home"
            home_dir.mkdir()
            config["env:HOME"] = str(home_dir)

        if "stdout" not in config:
            config["stdout"] = str(tmp_path / "server.log")

        if "stderr" not in config:
            config["stderr"] = "STDOUT"

        if notebook_dir is None:
            notebook_dir = tmp_path / "notebooks"
            notebook_dir.mkdir()
            config["cwd"] = str(notebook_dir)

        args = args or self.build_jupyter_server_arguments(
            port,
            base_url,
            token,
            app_name,
        )

        extra_args = config.pop("extra_args", [])

        handle = plib.start_process(command, *extra_args, *args, **config)

        self._handles += [handle]
        self._tmpdirs[handle] = str(tmp_path)
        self._notebook_dirs[handle] = str(notebook_dir)
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
    ) -> typing.Tuple[str]:
        """Build Some default Jupyter application arguments.

        If the ``app_name`` is not provided, it will be detected based on the rules
        in [#Get Jupyter App Name].
        """
        app_name = app_name or self.get_jupyter_app_name()
        return (
            "--no-browser",
            "--debug",
            f"--port={port}",
            f"--{app_name}.token={token}",
            f"--{app_name}.base_url={base_url}",
        )

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
        return osli.copy_files(*sorted(sources), notebook_dir)

    @keyword
    def copy_files_from_jupyter_directory(self, *src_and_dest: str, **kwargs) -> None:
        """Copy some files from the (temporary) jupyter server root.

        | = argument = | = default =                       |
        | ``nbserver`` | the most-recently launched server |

        Patterns will have the notebook directory prepended
        """
        nbserver = kwargs.get("nbserver", self._handles[-1])
        notebook_dir = Path(self._notebook_dirs[nbserver])
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        sources = [str(notebook_dir / src) for src in src_and_dest[:-1]]
        dest = src_and_dest[-1]
        return osli.copy_files(*sources, dest)

    @keyword
    def get_jupyter_directory(
        self,
        nbserver: typing.Optional[subprocess.Popen] = None,
    ) -> str:
        """Get the Jupyter contents directory.

        | = argument = | = default =                       |
        | ``nbserver`` | the most-recently launched server |
        """
        nbserver = nbserver if nbserver is not None else self._handles[-1]

        return self._notebook_dirs[nbserver]

    @keyword
    def wait_for_jupyter_server_to_be_ready(
        self,
        *nbservers: subprocess.Popen,
        **kwargs,
    ) -> int:
        """Wait for the most-recently started Jupyter server to be ready."""
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

        if ready != len(nbservers):
            message = (
                f"Only {ready} of {len(nbservers)} servers were ready after "
                f"{interval * retries}s. Last error: {type(error)} {error}"
            )
            raise RuntimeError(message)
        return ready

    @keyword
    def get_jupyter_server_url(
        self,
        nbserver: typing.Optional[subprocess.Popen] = None,
    ) -> str:
        """Get the given (or most recently-launched) server's URL."""
        nbh = nbserver or self._handles[-1]
        return f"http://127.0.0.1:{self._ports[nbh]}{self._base_urls[nbh]}"

    @keyword
    def get_jupyter_server_token(
        self,
        nbserver: typing.Optional[subprocess.Popen] = None,
    ) -> str:
        """Get the given (or most recently-launched) server's token."""
        nbh = nbserver or self._handles[-1]
        return self._tokens[nbh]

    @keyword
    def wait_for_new_jupyter_server_to_be_ready(
        self,
        command: typing.Optional[str] = None,
        *args,
        **config,
    ) -> subprocess.Popen:
        """Get the given (or most recently-launched) server's token.

        See [#Start New Jupyter Server|Start New Jupyter Server].
        """
        handle = self.start_new_jupyter_server(command, *args, **config)
        self.wait_for_jupyter_server_to_be_ready(handle)
        return handle

    @keyword
    def shut_down_jupyter_server(self, nbserver=None) -> int:
        """Gracefully shut down a Jupyter server started by [#Start New Jupyter Server|Start New Jupyter Server].

        If no ``handle`` is given, the last-started server will be shut down.
        """
        nbh = nbserver or self._handles[-1]
        url = self.get_jupyter_server_url(nbh)
        token = self.get_jupyter_server_token(nbh)

        try:
            urlopen(f"{url}api/shutdown?token={token}", data=[])
        except Exception as err:
            BuiltIn().log(err)
            return 0

        self._ports.pop(nbh)
        self._base_urls.pop(nbh)
        self._tokens.pop(nbh)

        return 1

    @keyword
    def clean_up_jupyter_server_files(self, nbserver=None) -> int:
        """Clean up the files owned by a started by [#Start New Jupyter Server|Jupyter Server].

        If no ``handle`` is given, the last-started server will be terminated.
        """
        nbh = nbserver or self._handles[-1]

        shutil.rmtree(self._tmpdirs[nbh], ignore_errors=True)

        self._tmpdirs.pop(nbh)

    @keyword
    def terminate_jupyter_server(self, nbserver=None) -> int:
        """Close a Jupyter server started by [#Start New Jupyter Server|Start New Jupyter Server].

        If no ``nbserver`` is given, the last-started server will be terminated.

        Waiting ``timeout`` to ensure all files/processes are freed before
        cleaning up temporary directories, if any.
        """
        plib = BuiltIn().get_library_instance("Process")

        nbh = nbserver or self._handles[-1]

        plib.terminate_process(nbh)

        self._handles.remove(nbh)

        return 1

    @keyword
    def terminate_all_jupyter_servers(self, timeout: str = "6s") -> int:
        """Close all Jupyter servers started by [#Start New Jupyter Server|Start New Jupyter Server].

        Waiting ``timeout`` after termination to ensure all files/processes are freed before
        cleaning up temporary directories.
        """
        was_shutdown = []
        was_terminated = []
        for nbh in self._handles:
            try:
                self.shut_down_jupyter_server(nbh)
                was_shutdown += [nbh]
            except Exception as err:
                BuiltIn().log(err)

        handles = list(self._handles)

        for nbh in handles:
            try:
                self.terminate_jupyter_server(nbh)
                was_terminated += [nbh]
            except Exception as err:
                BuiltIn().log(err)

        if was_shutdown or was_terminated:
            BuiltIn().sleep(timeout)

        tmpdir_handles = list(self._tmpdirs)

        for nbh in tmpdir_handles:
            self.clean_up_jupyter_server_files(nbh)

        return len(was_terminated)

    @keyword
    def get_unused_port(self) -> int:
        """Find an unused network port (could still create race conditions)."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
