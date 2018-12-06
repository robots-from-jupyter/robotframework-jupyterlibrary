import os
import shutil
import subprocess
import tempfile
import time
from os.path import join

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword
from six.moves.urllib.request import urlopen
from tornado.escape import json_decode


class ServerKeywords(LibraryComponent):
    _nbserver_handles = []
    _nbserver_tmpdirs = {}
    _nbserver_notebook_dirs = {}

    @keyword
    def start_new_jupyter_server(self, command="jupyter", *arguments, **configuration):
        """ Start a Jupyter server

            If not configured, the HOME environment variable and current
            working directory will be set to avoid leaking configuration
            between between runs (or the test instance) itself. These
            directories will be cleaned up after the server process is
            terminated.
        """
        plib = BuiltIn().get_library_instance("Process")
        if not arguments:
            arguments = self.build_jupyter_server_arguments()

        tmpdir = tempfile.mkdtemp()

        if "env:HOME" not in configuration:
            home_dir = join(tmpdir, "home")
            os.mkdir(home_dir)
            configuration["env:HOME"] = home_dir

        notebook_dir = configuration.get("cwd")
        if notebook_dir is None:
            notebook_dir = join(tmpdir, "notebooks")
            os.mkdir(notebook_dir)
            configuration["cwd"] = notebook_dir

        handle = plib.start_process("jupyter", *arguments, **configuration)

        self._nbserver_handles += [handle]
        self._nbserver_tmpdirs[handle] = tmpdir
        self._nbserver_notebook_dirs[handle] = notebook_dir

        return handle

    @keyword
    def build_jupyter_server_arguments(self):
        """ Some default jupyter arguments
        """
        return ["notebook", "--no-browser"]

    @keyword
    def copy_files_to_jupyter_directory(self, *sources, **kwargs):
        """ Copy some files into the (temporary) jupyter server root
        """
        nbserver = kwargs.get("nbserver", self._nbserver_handles[-1])
        notebook_dir = self._nbserver_notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        osli.copy_files(*(list(sources) + [notebook_dir]))

    @keyword
    def copy_files_from_jupyter_directory(self, *sources_and_destinations, **kwargs):
        """ Copy some files from the (temporary) jupyter server root

            Patterns will have the notebook directory prepended
        """
        nbserver = kwargs.get("nbserver", self._nbserver_handles[-1])
        notebook_dir = self._nbserver_notebook_dirs[nbserver]
        BuiltIn().import_library("OperatingSystem")
        osli = BuiltIn().get_library_instance("OperatingSystem")
        sources = [join(notebook_dir, src) for src in sources_and_destinations[:-1]]
        dest = sources_and_destinations[-1]
        osli.copy_files(*sources + [dest])

    @keyword
    def get_jupyter_directory(self, nbserver=None):
        nbserver = nbserver if nbserver is not None else self._nbserver_handles[-1]
        return self._nbserver_notebook_dirs[nbserver]

    @keyword
    def wait_for_jupyter_server_to_be_ready(self, *nbservers, **kwargs):
        """  Wait for the most-recently started Jupyter server to be ready
        """
        interval = float(kwargs.get("interval", 0.5))
        retries = int(kwargs.get("retries", 60))

        plib = BuiltIn().get_library_instance("Process")

        if not nbservers:
            if not self._nbserver_handles:
                return 0
            nbservers = [self._nbserver_handles[-1]]

        ready = 0
        last_error = None

        while retries and ready != len(nbservers):
            retries -= 1
            ready = 0

            try:
                nbservers_json = self.get_jupyter_servers()
                for nbhandle in nbservers:
                    nbpopen = plib.get_process_object(nbhandle)
                    nbj = nbservers_json[nbpopen.pid]
                    urlopen("{url}favicon.ico".format(**nbj))
                    ready += 1
            except Exception as err:
                time.sleep(interval)
                last_error = err

        assert ready == len(
            nbservers
        ), "Only {} of {} servers were ready after {}s. Last error: {} {}".format(
            ready, len(nbservers), interval * retries, type(last_error),
            last_error
        )
        return ready

    @keyword
    def wait_for_new_jupyter_server_to_be_ready(
        self, command=None, *arguments, **configuration
    ):
        handle = self.start_new_jupyter_server(command, *arguments, **configuration)
        self.wait_for_jupyter_server_to_be_ready(handle)
        return handle

    @keyword
    def terminate_all_jupyter_servers(self, kill=False):
        """ Close all Jupyter servers started by JupyterLibrary
        """
        plib = BuiltIn().get_library_instance("Process")
        terminated = 0
        for handle in self._nbserver_handles:
            plib.terminate_process(handle, kill=kill)
            terminated += 1

        for tmpdir in self._nbserver_tmpdirs.values():
            shutil.rmtree(tmpdir)

        self._nbserver_handles = []
        self._nbserver_tmpdirs = {}

        return terminated

    @keyword
    def get_jupyter_server_info(self, nbserver=None):
        nbserver = nbserver or self._nbserver_handles[-1]
        plib = BuiltIn().get_library_instance("Process")
        nbpopen = plib.get_process_object(nbserver)
        nbj = self.get_jupyter_servers()[nbpopen.pid]
        return nbj

    def get_jupyter_servers(self):
        nbservers = list(
            map(
                json_decode,
                subprocess.check_output(["jupyter", "notebook", "list", "--json"])
                .decode("utf-8")
                .strip()
                .split("\n"),
            )
        )
        return {nbserver["pid"]: nbserver for nbserver in nbservers}
