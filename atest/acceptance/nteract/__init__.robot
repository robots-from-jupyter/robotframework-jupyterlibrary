*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Suite Teardown    Terminate All Jupyter Servers
Force Tags        client:nteract_on_jupyter
Library           JupyterLibrary
