*** Settings ***
Documentation       Command keywords for Jupyter Classic

Resource            JupyterLibrary/clients/classic/Selectors.resource


*** Keywords ***
Execute Notebook Classic Command
    [Documentation]    Use the Notebook Classic Command Pop-up
    ...    to run a command and ``accept`` any resulting dialogs, then ``close``
    ...    the Command Palette.
    [Arguments]    ${command}
    Click Element    css:${JNC CSS CMD BUTTON}
    Input Text    css:${JNC CSS CMD INPUT}    ${command}
    Click Element    css:${JNC CSS CMD ITEM}
