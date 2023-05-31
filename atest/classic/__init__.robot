*** Settings ***
Documentation       Tests of Jupyter Classic client keywords

Library             JupyterLibrary

Suite Setup         Set Up Classic Suite
Suite Teardown      Terminate All Jupyter Servers

Force Tags          client:classic


*** Keywords ***
Set Up Classic Suite
    [Documentation]    Configure the top-level app and start the server
    Wait For New Jupyter Server To Be Ready    jupyter-notebook
