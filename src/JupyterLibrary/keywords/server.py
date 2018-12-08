import os
import shutil
import socket
import tempfile
import time
from os.path import join

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword
from six.moves.urllib.request import urlopen


class ServerKeywords(LibraryComponent):
    _handles = []
    _tmpdirs = {}
    _notebook_dirs = {}
    _ports = {}
    _base_urls = {}

    @keyword
    def start_new_jupyter_server(
        self, command=None, port=None, base_url=None, *args, **config
    ):
        """ Start a Jupyter server

            If not configured, the HOME environment variable and current
            working directory will be set to avoid leaking configuration
            between between runs (or the test instance) itself. These
            directories will be cleaned up after the server process is
            terminated.
        """
        command = command or "jupyter"
        port = port or self.get_unused_port()
        base_url = base_url or "/@rf/"
        args = args or self.build_jupyter_server_arguments(port, base_url)

        plib = BuiltIn().get_library_instance("Process")

        tmpdir = tempfile.mkdtemp()

        if "env:HOME" not in config:
            home_dir = join(tmpdir, "home")
            os.mkdir(home_dir)
            config["env:HOME"] = home_dir

        notebook_dir = config.get("cwd")
        if notebook_dir is None:
            notebook_dir = join(tmpdir, "notebooks")
            os.mkdir(notebook_dir)
            config["cwd"] = notebook_dir

        handle = plib.start_process(command, *args, **config)

        self._handles += [handle]
        self._tmpdirs[handle] = tmpdir
        self._notebook_dirs[handle] = notebook_dir
        self._ports[handle] = port
        self._base_urls[handle] = base_url

        return handle

    @keyword
    def build_jupyter_server_arguments(self, port, base_url):
        """ Some default jupyter arguments
        """
        return [
            "notebook",
            "--no-browser",
            "--port",
            port,
            "--NotebookApp.base_url",
            base_url,
        ]

    @keyword
    def copy_files_to_jupyter_directory(self, *sources, **kwargs):
        """ Copy some files into the (temporary) jupyter server root
        """
        nbserver = kwargs.get("nbserver", self._handles[-1])
        notebook_dir = self._notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        osli.copy_files(*(list(sources) + [notebook_dir]))

    @keyword
    def copy_files_from_jupyter_directory(self, *src_and_dest, **kwargs):
        """ Copy some files from the (temporary) jupyter server root

            Patterns will have the notebook directory prepended
        """
        nbserver = kwargs.get("nbserver", self._handles[-1])
        notebook_dir = self._notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        sources = [join(notebook_dir, src) for src in src_and_dest[:-1]]
        dest = src_and_dest[-1]
        osli.copy_files(*sources + [dest])

    @keyword
    def get_jupyter_directory(self, nbserver=None):
        nbserver = nbserver if nbserver is not None else self._handles[-1]
        return self._notebook_dirs[nbserver]

    @keyword
    def wait_for_jupyter_server_to_be_ready(self, *nbservers, **kwargs):
        """  Wait for the most-recently started Jupyter server to be ready
        """
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
                    urlopen("{}favicon.ico".format(self.get_jupyter_server_url(nbh)))
                    ready += 1
            except Exception as _error:
                time.sleep(interval)
                error = _error

        assert ready == len(
            nbservers
        ), "Only {} of {} servers were ready after {}s. Last error: {} {}".format(
            ready, len(nbservers), interval * retries, type(error), error
        )
        return ready

    @keyword
    def get_jupyter_server_url(self, nbserver=None):
        nbh = nbserver or self._handles[-1]
        return "http://localhost:{}{}".format(self._ports[nbh], self._base_urls[nbh])

    @keyword
    def wait_for_new_jupyter_server_to_be_ready(self, command=None, *args, **config):
        handle = self.start_new_jupyter_server(command, *args, **config)
        self.wait_for_jupyter_server_to_be_ready(handle)
        return handle

    @keyword
    def terminate_all_jupyter_servers(self):
        """ Close all Jupyter servers started by JupyterLibrary
        """
        plib = BuiltIn().get_library_instance("Process")
        terminated = 0
        for handle in self._handles:
            plib.terminate_process(handle, kill=True)
            terminated += 1

        for tmpdir in self._tmpdirs.values():
            shutil.rmtree(tmpdir)

        self._handles = []
        self._tmpdirs = {}

        return terminated

    @keyword
    def get_unused_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
