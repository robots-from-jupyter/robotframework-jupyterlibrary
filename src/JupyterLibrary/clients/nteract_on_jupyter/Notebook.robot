*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot
Resource   JupyterLibrary/common/CodeMirror.robot

*** Keywords ***
Add and Run nteract Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    ${creators} =  Get WebElements    css:${NOJ CSS CREATOR}
    Mouse Over  ${creators[-1]}
    Click Element    css:${NOJ CSS CREATOR}:hover ${NOJ CSS ADD CODE CELL}
    ${cells} =  Get WebElements    css:${NOJ CSS CELL INPUT}
    Click Element    ${cells[-1]}
    Set CodeMirror Value  ${NOJ CSS ACTIVE CELL INPUT}  ${code}
    Run Current nteract Code Cell

Run Current nteract Code Cell
    Mouse Over    css:${NOJ CSS EXECUTE}
    Click Element    css:${NOJ CSS EXECUTE}

Wait Until nteract Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain    ${NOJ TEXT BUSY PROMPT}
