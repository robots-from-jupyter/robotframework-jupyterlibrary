*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Test Teardown     Close All Browsers
Library           JupyterLibrary
Library           Process
Resource          JupyterLibrary/resources/jupyterlab/Shell.robot

*** Test Cases ***
Open JupyterLab
    Open JupyterLab

Get Help
    Open JupyterLab
    Click JupyterLab Menu    Help
    Click JupyterLab Menu Item    About JupyterLab
    Click Element    css:${JLAB CSS ACCEPT}

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Processes
