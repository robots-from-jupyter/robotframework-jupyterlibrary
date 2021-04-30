*** Settings ***
Suite Setup       Set Up JupyterLab Suite
Suite Teardown    Terminate All Jupyter Servers
Force Tags        client:jupyterlab
Library           JupyterLibrary

*** Keywords ***
Set Up JupyterLab Suite
    Wait for New Jupyter Server to be Ready
    Set Screenshot Directory    ${OUTPUT DIR}${/}lab
