*** Settings ***
Test Teardown     Close All Browsers
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on nteract
    Open nteract
    Launch a new nteract Notebook
    Add and Run nteract Code Cell    print("hello world")
    Wait Until nteract Kernel Is Idle
    Current nteract Cell Output Should Contain    hello world
    Capture Page Screenshot    nteract${/}ipython.png
