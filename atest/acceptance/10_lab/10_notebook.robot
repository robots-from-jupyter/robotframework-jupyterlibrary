*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Test Teardown     Close All Browsers
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook
    Open JupyterLab
    Launch a new JupyterLab Document
    Add and Run Cell    print("hello world")
    Wait Until Kernel Is Idle
    Capture Page Screenshot    ipython.png

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Processes
