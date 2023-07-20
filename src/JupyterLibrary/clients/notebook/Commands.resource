*** Settings ***
Documentation       Command keywords for Jupyter Notebook

Resource            JupyterLibrary/clients/notebook/Selectors.resource


*** Keywords ***
Execute Notebook Command
    [Documentation]    Use the Jupyter Notebook Command Pop-up
    ...    to run a command and ``accept`` any resulting dialogs, then ``close``
    ...    the Command Palette.
    [Arguments]    ${command}
    Click Element    css:${JNB CSS CMD BUTTON}
    Input Text    css:${JNB CSS CMD INPUT}    ${command}
    Click Element    css:${JNB CSS CMD ITEM}
