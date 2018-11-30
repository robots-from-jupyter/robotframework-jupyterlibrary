import subprocess
import time
from six.moves.urllib.request import urlopen

from robot.libraries.BuiltIn import BuiltIn
from tornado.escape import json_decode

from SeleniumLibrary.base import keyword, LibraryComponent


class NBServer(object):
    process = None


class ServerKeywords(LibraryComponent):
    _nbserver_handles = []

    @keyword
    def start_new_jupyter_server(self, command="jupyter", *arguments, **configuration):
        """ Start a Jupyter server
        """
        plib = BuiltIn().get_library_instance('Process')
        if not arguments:
            arguments = self.build_jupyter_server_arguments()

        handle = plib.start_process("jupyter", *arguments, **configuration)
        self._nbserver_handles += [handle]
        return handle

    @keyword
    def build_jupyter_server_arguments(self):
        return ["notebook", "--no-browser"]

    @keyword
    def wait_for_jupyter_server_to_be_ready(self, *nbservers, **kwargs):
        """  Wait for the most-recently started Jupyter server to be ready
        """
        interval = float(kwargs.get("interval", 0.25))
        retries = int(kwargs.get("retries", 20))

        plib = BuiltIn().get_library_instance('Process')

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

        assert ready == len(nbservers), (
            "Only {} of {} servers were ready: {}".format(
                ready, len(nbservers), last_error
            ))
        return ready

    @keyword
    def terminate_all_jupyter_servers(self, kill=False):
        """ Close all Jupyter servers started by JupyterLibrary
        """
        plib = BuiltIn().get_library_instance('Process')
        terminated = 0
        for handle in self._nbserver_handles:
            plib.terminate_process(handle, kill=kill)
            terminated += 1

        self._nbserver_handles = []

        return terminated

    def get_jupyter_servers(self):
        nbservers = list(map(json_decode, subprocess.check_output(
            ["jupyter", "notebook", "list", "--json"]
        ).decode("utf-8").strip().split("\n")))
        return {nbserver["pid"]: nbserver for nbserver in nbservers}
