*** Settings ***
Documentation       Does the baseline Lab Shell work?

Library             Process
Library             JupyterLibrary

Suite Teardown      Close All Browsers
Test Teardown       Reset JupyterLab And Close


*** Test Cases ***
Open JupyterLab
    [Documentation]    Does Lab open?
    Open JupyterLab    ${BROWSER}

Get Help
    [Documentation]    Can we get help?
    Open JupyterLab    ${BROWSER}
    Open With JupyterLab Menu    Help    About JupyterLab
    Capture Element Screenshot    css:.jp-Dialog-content    00-about.png
    Click Element    css:${JLAB CSS ACCEPT}
