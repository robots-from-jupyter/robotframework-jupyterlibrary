*** Settings ***
Suite Teardown    Run Keyword and Ignore Error    Close All Browsers
Test Teardown     Run Keyword and Ignore Error    Reset JupyterLab and Close
Default Tags      settings
Library           JupyterLibrary
Library           Process

*** Variables ***
${PACKAGE}        @jupyterlab/apputils-extension
${PLUGIN}         palette

*** Test Cases ***
Command Palette
    [Documentation]    Verify settings and command palette
    Open JupyterLab    ${BROWSER}
    Disable JupyterLab Modal Command Palette
    ${config} =    Get JupyterLab Plugin Settings    ${PACKAGE}    ${PLUGIN}
    Should Be True    not ${config["modal"]}
    Enable JupyterLab Modal Command Palette
    ${config} =    Get JupyterLab Plugin Settings    ${PACKAGE}    ${PLUGIN}
    Should Be True    ${config["modal"]}
