*** Settings ***
Documentation       Tests of JupyterLab client keywords

Library             JupyterLibrary

Suite Setup         Set Up JupyterLab Suite
Suite Teardown      Tear Down JupyterLab Suite

Force Tags          client:jupyterlab


*** Keywords ***
Set Up JupyterLab Suite
    [Documentation]    Get ready to test JupyterLab with a sever
    Wait For New Jupyter Server To Be Ready

Tear Down JupyterLab Suite
    [Documentation]    Clean up after JupyterLab
    Run Keyword And Ignore Error
    ...    Execute JupyterLab Command    Shut Down All Kernels
    Terminate All Jupyter Servers
