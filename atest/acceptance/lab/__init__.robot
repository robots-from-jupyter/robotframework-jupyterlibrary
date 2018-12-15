*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Suite Teardown    Terminate All Jupyter Servers
Force Tags        jupyterlab
Library           JupyterLibrary
