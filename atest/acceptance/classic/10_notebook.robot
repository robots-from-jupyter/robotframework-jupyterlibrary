*** Settings ***
Test Teardown     Close All Browsers
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on Classic
    Open Notebook Classic
    Launch a new Notebook Classic Notebook
    Add and Run Notebook Classic Code Cell
    Wait Until Notebook Classic Kernel Is Idle
    Capture Page Screenshot    classic${/}ipython.png
