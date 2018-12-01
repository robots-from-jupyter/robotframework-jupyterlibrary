*** Settings ***
Documentation     Run JupyterLab commands
Resource   JupyterLibrary/resources/jupyterlab/Selectors.robot


*** Keywords ***
Execute JupyterLab Command
    [Arguments]    ${command}  ${accept}=${True}  ${close}=${True}
    [Documentation]    Use the JupyterLab Command Palette to run a command
    Maybe accept a prompt
    Maybe Open JupyterLab Sidebar  command-palette
    Input Text    css:${JLAB CSS CMD INPUT}    ${command}
    Wait Until Page Contains Element    css:${JLAB CSS CMD ITEM}
    Click Element    css:${JLAB CSS CMD ITEM}
    Run Keyword If  ${accept}  Maybe Accept a Prompt
    Run Keyword If  ${close}  Maybe Close Sidebar

Reset Application State and Close
    [Documentation]    Try to clean up after doing some things to the JupyterLab state
    Execute JupyterLab Command    Reset Application State
    Close Browser
