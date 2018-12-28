*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot
Resource   JupyterLibrary/common/CodeMirror.robot

*** Keywords ***
Add and Run nteract Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    ${creators} =  Get WebElements    css:${NOJ CSS CREATOR}
    Set nteract Status Bar Pointer Events  "none"
    Scroll To End Of Page
    Scroll Element Into View  ${creators[-1]}
    Mouse Over  ${creators[-1]}
    Click Element    css:${NOJ CSS CREATOR}:hover ${NOJ CSS ADD CODE CELL}
    ${cells} =  Get WebElements    css:${NOJ CSS CELL INPUT}
    Scroll To End Of Page
    Mouse Over  ${cells[-1]}
    Click Element    ${cells[-1]}
    Set CodeMirror Value  ${NOJ CSS ACTIVE CELL INPUT}  ${code}
    Set nteract Status Bar Pointer Events  null
    Run Current nteract Code Cell

Run Current nteract Code Cell
    Press Keys   css:body  CTRL+ENTER


Wait Until nteract Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain    ${NOJ TEXT BUSY PROMPT}

Set nteract Status Bar Pointer Events
    [Arguments]  ${pointerevents}=null
    Execute JavaScript
    ...   document.querySelector("${NOJ CSS STATUS BAR}").pointerEvents = ${pointerevents}

Scroll To End Of Page
    Execute JavaScript
    ...   document.querySelector("body").scrollTop = 999999
