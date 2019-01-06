*** Settings ***
Resource   JupyterLibrary/clients/notebook/Selectors.robot

*** Keywords ***
Execute Notebook Classic Command
    [Arguments]    ${command}  ${accept}=${True}  ${close}=${True}
    [Documentation]    Use the Notebook Classic Command Pop-up
    ...   to run a command and ``accept`` any resulting dialogs, then ``close``
    ...   the Command Palette.
    Click Element  css:${JNC CSS CMD BUTTON}
    Input Text    css:${JNC CSS CMD INPUT}    ${command}
    Click Element    css:${JNC CSS CMD ITEM}
