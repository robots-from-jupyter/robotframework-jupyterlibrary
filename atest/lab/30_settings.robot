*** Settings ***
Documentation       Test JupyterLab Advanced Settings

Library             Process
Library             JupyterLibrary

Suite Teardown      Run Keyword And Ignore Error    Close All Browsers
Test Teardown       Run Keyword And Ignore Error    Reset JupyterLab And Close

Default Tags        settings


*** Variables ***
${PACKAGE}      @jupyterlab/apputils-extension
${PLUGIN}       palette


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
