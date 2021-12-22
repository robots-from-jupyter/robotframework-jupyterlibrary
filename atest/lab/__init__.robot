*** Settings ***
Library             JupyterLibrary

Suite Setup         Set Up JupyterLab Suite
Suite Teardown      Tear Down JupyterLab Suite

Force Tags          client:jupyterlab

*** Keywords ***
Set Up JupyterLab Suite
    Wait for New Jupyter Server to be Ready

Tear Down JupyterLab Suite
    Run Keyword And Ignore Error
    ...    Execute JupyterLab Command    Shut Down All Kernels
    Terminate All Jupyter Servers
