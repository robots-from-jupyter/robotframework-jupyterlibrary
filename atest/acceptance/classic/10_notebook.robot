*** Settings ***
Test Teardown     Close All Browsers
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook
    Open Jupyter Notebook Classic
    Launch a new Jupyter Notebook Classic Notebook
    Capture Page Screenshot    ipython.png
