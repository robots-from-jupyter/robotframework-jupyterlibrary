*** Settings ***
Library             JupyterLibrary
Library             Process

Suite Teardown      Close All Browsers
Test Teardown       Reset JupyterLab and Close

*** Test Cases ***
Open JupyterLab
    Open JupyterLab    ${BROWSER}

Get Help
    Open JupyterLab    ${BROWSER}
    Open With JupyterLab Menu    Help    About JupyterLab
    Capture Element Screenshot    css:.jp-Dialog-content    00-about.png
    Click Element    css:${JLAB CSS ACCEPT}
