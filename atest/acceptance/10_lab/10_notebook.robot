*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Test Teardown     Reset JupyterLab and Close
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook
    Open JupyterLab
    Launch a new JupyterLab Document
    Add and Run Cell    print("hello world")
    Wait Until Kernel Is Idle
    Capture Page Screenshot    ipython.png

IPython Notebook Outputs
    Open JupyterLab
    Launch a new JupyterLab Document
    Add and Run Cell    print("hello world")
    Wait Until Kernel Is Idle
    Screenshot Each Output of Active Document    ${OUTPUT_DIR}${/}ipython

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Processes
