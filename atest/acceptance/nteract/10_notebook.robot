*** Settings ***
Test Teardown     Close All Browsers
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on nteract
    Open nteract    ${BROWSER}
    Launch a new nteract Notebook
    Add and Run nteract Code Cell    print("hello world")
    Wait Until nteract Kernel Is Idle
    Current nteract Cell Output Should Contain    hello world
    Capture Page Screenshot    nteract${/}ipython.png
    Save nteract Notebook

IPython Notebook Outputs on nteract
    Open nteract    ${BROWSER}
    Launch a new nteract Notebook
    : FOR    ${i}    IN RANGE    ${10}
    \    Add and Run nteract Code Cell    print("${i} hello world " * ${i ** 2})
    Wait Until nteract Kernel Is Idle
    Screenshot Each Output of Active nteract Document    nteract${/}ipython_outputs${/}
    Save nteract Notebook
