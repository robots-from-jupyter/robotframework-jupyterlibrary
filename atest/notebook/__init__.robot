*** Settings ***
Documentation       Tests of Jupyter Notebook client keywords

Library             JupyterLibrary

Suite Setup         Set Up Notebook Suite
Suite Teardown      Terminate All Jupyter Servers

Force Tags          client:notebook


*** Keywords ***
Set Up Notebook Suite
    [Documentation]    Configure the top-level app and start the server
    Wait For New Jupyter Server To Be Ready    jupyter-notebook
    ...    stdout=${OUTPUT_DIR}${/}server.log
