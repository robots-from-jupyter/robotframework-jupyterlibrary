*** Settings ***
Suite Setup       Set Up JupyterLab Suite
Suite Teardown    Tear Down JupyterLab Suite
Force Tags        client:jupyterlab
Library           JupyterLibrary

*** Keywords ***
Set Up JupyterLab Suite
    Wait for New Jupyter Server to be Ready
    Set Screenshot Directory    ${OUTPUT DIR}${/}lab

Tear Down JupyterLab Suite
    Run Keyword and Ignore Error
    ...    Execute JupyterLab Command    Shut Down All Kernels
    Terminate All Jupyter Servers
