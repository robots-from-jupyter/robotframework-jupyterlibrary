*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot
Library  JupyterLibrary

*** Keywords ***
Add and Run nteract Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    ${creators} =  Get WebElements    css:${NOJ CSS CREATOR}
    Mouse Over  ${creators[-1]}
    Click Element    css:${NOJ CSS CREATOR}:hover ${NOJ CSS ADD CODE CELL}
    Click Element    css:${NOJ CSS CELL INPUT}
    Execute JavaScript    document.querySelector("${NOJ CSS CELL INPUT}").CodeMirror.setValue(`${code}`)
    Click Element    css:${NOJ CSS EXECUTE}

Wait Until nteract Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain    ${NOJ TEXT BUSY PROMPT}
