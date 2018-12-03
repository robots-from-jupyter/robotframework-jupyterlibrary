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
    : FOR    ${i}    IN RANGE    ${10}
    \    Add and Run Cell    print("${i} hello world " * ${i ** 2})
    Wait Until Kernel Is Idle
    Screenshot Each Output of Active Document    ${OUTPUT_DIR}${/}ipython_outputs/

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Processes
