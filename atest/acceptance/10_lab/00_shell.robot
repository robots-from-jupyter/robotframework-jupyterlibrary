*** Settings ***
Suite Setup       Wait for New Jupyter Server to be Ready
Test Teardown     Close All Browsers
Library           JupyterLibrary
Library           Process

*** Test Cases ***
Open JupyterLab
    Open JupyterLab

Get Help
    Open JupyterLab
    Click JupyterLab Menu    Help
    Click JupyterLab Menu Item    About JupyterLab
    Capture Element Screenshot    css:.jp-Dialog-content    ${OUTPUT_DIR}${/}about.png
    Click Element    css:${JLAB CSS ACCEPT}

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Processes
