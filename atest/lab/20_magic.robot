*** Settings ***
Documentation       Tests of the IPython magic

Library             Process
Library             JupyterLibrary

Suite Teardown      Run Keyword And Ignore Error    Close All Browsers
Test Teardown       Run Keyword And Ignore Error    Reset JupyterLab And Close

Default Tags        notebook    magic


*** Variables ***
${LOAD EXT}             %reload_ext JupyterLibrary
${IND}                  ${SPACE.__mul__(4)}
@{MAGIC}
...                     %%robot
...                     *** Tasks ***
...                     Log Something
...                     ${IND}Log${IND}Something
${NEXT SCREENSHOT}      ${0}


*** Test Cases ***
IPython Magic On Lab
    [Documentation]    Verify the IPython magic works in JupyterLab.
    Open JupyterLab    ${BROWSER}
    Launch A New JupyterLab Document
    Add And Run JupyterLab Code Cell    ${LOAD EXT}
    Add And Run JupyterLab Code Cell    @{MAGIC}
    Log    TODO: https://github.com/robots-from-jupyter/robotframework-jupyterlibrary/issues/54
    # Wait For And Click Text    Formatted Robot Code
    Wait For And Click Text    returned 0
    Save JupyterLab Notebook


*** Keywords ***
Wait For And Click Text
    [Documentation]    Verify clicking some text works.
    [Arguments]    ${canary}
    ${sel} =    Set Variable    xpath://*[contains(text(), '${canary}')]
    Wait Until Element Is Visible    ${sel}
    Click Element    ${sel}
    Capture Page Screenshot    lab${/}20-00-magic-${NEXT SCREENSHOT}-${canary}.png
    Set Test Variable    ${NEXT SCREENSHOT}    ${NEXT SCREENSHOT.__add__(1)}
