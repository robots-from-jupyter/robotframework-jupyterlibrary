*** Settings ***
Resource   JupyterLibrary/clients/notebook/Selectors.robot
Resource   JupyterLibrary/common/CodeMirror.robot

*** Keywords ***
Add and Run Notebook Classic Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    Click Element    css:${JNC CSS NB TOOLBAR} ${JNC CSS ICON ADD}
    Sleep    0.1s
    ${cell} =  Get WebElement  css:${JNC CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JNC CSS ACTIVE INPUT}  ${code}
    Run Current Notebook Classic Code Cell
    Click Element   ${cell}

Wait Until Notebook Classic Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JNC CSS NB KERNEL BUSY}
    Wait Until Page Does Not Contain    ${JNC TEXT BUSY PROMPT}

Run Current Notebook Classic Code Cell
    Click Element    css:${JNC CSS NB TOOLBAR} ${JNC CSS ICON RUN}
