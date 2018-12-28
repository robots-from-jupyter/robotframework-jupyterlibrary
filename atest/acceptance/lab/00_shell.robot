*** Settings ***
Suite Teardown    Close All Browsers
Test Teardown     Reset JupyterLab and Close
Library           JupyterLibrary
Library           Process

*** Test Cases ***
Open JupyterLab
    Open JupyterLab    ${BROWSER}

Get Help
    Open JupyterLab    ${BROWSER}
    Open With JupyterLab Menu    Help    About JupyterLab
    Capture Element Screenshot    css:.jp-Dialog-content    lab${/}about.png
    Click Element    css:${JLAB CSS ACCEPT}
