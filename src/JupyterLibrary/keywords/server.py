import os
import shutil
import socket
import tempfile
import time
from os.path import join
from uuid import uuid4

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword
from six.moves.urllib.request import urlopen


class ServerKeywords(LibraryComponent):
    _handles = []
    _tmpdirs = {}
    _notebook_dirs = {}
    _ports = {}
    _base_urls = {}
    _tokens = {}

    @keyword
    def start_new_jupyter_server(
        self,
        command=None,
        port=None,
        base_url=None,
        notebook_dir=None,
        token=None,
        *args,
        **config,
    ):
        """ Start a Jupyter server

            If not configured, the HOME environment variable and current
            working directory will be set to avoid leaking configuration
            between between runs (or the test instance) itself. These
            directories will be cleaned up after the server process is
            terminated.
        """
        command = command or "jupyter-notebook"
        port = port or self.get_unused_port()
        base_url = base_url or "/@rf/"
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

        args = args or self.build_jupyter_server_arguments(port, base_url, token)

        handle = plib.start_process(command, *args, **config)

        self._handles += [handle]
        self._tmpdirs[handle] = tmpdir
        self._notebook_dirs[handle] = notebook_dir
        self._ports[handle] = port
        self._base_urls[handle] = base_url
        self._tokens[handle] = token

        return handle

    @keyword
    def build_jupyter_server_arguments(self, port, base_url, token):
        """ Some default jupyter arguments
        """
        return [
            "--no-browser",
            "--debug",
            "--port={}".format(port),
            "--NotebookApp.token='{}'".format(token),
            "--NotebookApp.base_url='{}'".format(base_url),
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
                    urlopen(self.get_jupyter_server_url(nbh))
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
    def get_jupyter_server_token(self, nbserver=None):
        nbh = nbserver or self._handles[-1]
        return self._tokens[nbh]

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

        self.wait_for_jupyter_server_to_be_ready()

        terminated = 0
        shutdown = 0
        for nbh in self._handles:
            url = self.get_jupyter_server_url(nbh)
            token = self.get_jupyter_server_token(nbh)
            try:
                urlopen("{}api/shutdown?token={}".format(url, token), data=[])
                shutdown += 1
            except Exception as err:
                BuiltIn().log(err)

        if shutdown:
            for nbh in self._handles:
                try:
                    plib.terminate_process(nbh, kill=True)
                    terminated += 1
                except Exception as err:
                    BuiltIn().log(err)

        # give processes a mo to shutdown
        if terminated or shutdown:
            BuiltIn().sleep("5s")
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
    def get_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
