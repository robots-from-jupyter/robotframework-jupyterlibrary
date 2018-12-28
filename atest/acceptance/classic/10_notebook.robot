*** Settings ***
Test Teardown     Close All Browsers
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on Classic
    Open Notebook Classic    ${BROWSER}
    Launch a new Notebook Classic Notebook
    Add and Run Notebook Classic Code Cell    print("hello world")
    Wait Until Notebook Classic Kernel Is Idle
    Current Notebook Classic Cell Output Should Contain    hello world
    Capture Page Screenshot    classic${/}ipython.png

IPython Notebook Outputs on Classic
    Open Notebook Classic    ${BROWSER}
    Launch a new Notebook Classic Notebook
    : FOR    ${i}    IN RANGE    ${10}
    \    Add and Run Notebook Classic Code Cell    print("${i} hello world " * ${i ** 2})
    Wait Until Notebook Classic Kernel Is Idle
    Screenshot Each Output of Active Notebook Classic Document    classic${/}ipython_outputs${/}
