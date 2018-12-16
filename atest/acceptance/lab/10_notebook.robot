*** Settings ***
Suite Teardown    Close All Browsers
Test Teardown     Reset JupyterLab and Close
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on Lab
    Open JupyterLab
    Launch a new JupyterLab Document
    Add and Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Capture Page Screenshot    lab${/}ipython.png

IPython Notebook Outputs on Lab
    Open JupyterLab
    Launch a new JupyterLab Document
    : FOR    ${i}    IN RANGE    ${10}
    \    Add and Run JupyterLab Code Cell    print("${i} hello world " * ${i ** 2})
    Wait Until JupyterLab Kernel Is Idle
    Screenshot Each Output of Active JupyterLab Document    lab${/}ipython_outputs${/}
