*** Settings ***
Suite Teardown    Run Keyword and Ignore Error    Close All Browsers
Test Teardown     Run Keyword and Ignore Error    Reset JupyterLab and Close
Default Tags      notebook    magic
Library           JupyterLibrary
Library           Process

*** Variables ***
${LOAD EXT}       %reload_ext JupyterLibrary
${IND}            ${SPACE.__mul__(4)}
@{MAGIC}
...               %%robot
...               *** Tasks ***
...               Log Something
...               ${IND}Log${IND}Something
${NEXT SCREENSHOT}    ${0}

*** Test Cases ***
IPython Magic on Lab
    Open JupyterLab    ${BROWSER}
    Launch a new JupyterLab Document
    Add and Run JupyterLab Code Cell    ${LOAD EXT}
    Add and Run JupyterLab Code Cell    @{MAGIC}
    Wait for and Click Text    Formatted Robot Code
    Wait for and Click Text    returned 0
    Save JupyterLab Notebook

*** Keywords ***
Wait for and Click Text
    [Arguments]    ${canary}
    ${sel} =    Set Variable    xpath://*[contains(text(), '${canary}')]
    Wait Until Page Contains Element    ${sel}
    Click Element    ${sel}
    Capture Page Screenshot    lab${/}magic-${NEXT SCREENSHOT}-${canary}.png
    Set Test Variable    ${NEXT SCREENSHOT}    ${NEXT SCREENSHOT.__add__(1)}
