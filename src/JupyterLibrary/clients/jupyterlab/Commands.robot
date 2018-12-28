*** Settings ***
Resource   JupyterLibrary/clients/jupyterlab/Selectors.robot

*** Keywords ***
Execute JupyterLab Command
    [Arguments]    ${command}  ${accept}=${True}  ${close}=${True}
    [Documentation]    Use the JupyterLab
    ...   [https://jupyterlab.readthedocs.io/en/stable/user/commands.html|Command Palette]
    ...   to run a command and ``accept`` any resulting dialogs, then ``close``
    ...   the Command Palette.
    Maybe accept a JupyterLab prompt
    Maybe Open JupyterLab Sidebar  Commands
    Input Text    css:${JLAB CSS CMD INPUT}    ${command}
    Wait Until Page Contains Element    css:${JLAB CSS CMD ITEM}
    Click Element    css:${JLAB CSS CMD ITEM}
    Run Keyword If  ${accept}  Maybe Accept a JupyterLab Prompt
    Run Keyword If  ${close}  Maybe Close JupyterLab Sidebar

Reset JupyterLab and Close
    [Documentation]    Try to clean up after doing some things to the JupyterLab
    ...    open in the current browser, then close the browser.
    Execute JupyterLab Command    Reset Application State
    Close Browser
