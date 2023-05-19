*** Settings ***
Documentation       Notebook keywords for Jupyter Classic

Resource            JupyterLibrary/clients/classic/Selectors.resource
Resource            JupyterLibrary/common/CodeMirror.resource


*** Keywords ***
Add And Run Notebook Classic Code Cell
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    [Arguments]    ${code}=print("hello world")
    Click Element    css:${JNC CSS NB TOOLBAR} ${JNC CSS ICON ADD}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JNC CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JNC CSS ACTIVE INPUT}    ${code}
    Run Current Notebook Classic Code Cell
    Click Element    ${cell}

Wait Until Notebook Classic Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JNC CSS NB KERNEL BUSY}
    Wait Until Page Does Not Contain    ${JNC TEXT BUSY PROMPT}

Run Current Notebook Classic Code Cell
    [Documentation]    Run the currently-selected code cell
    Click Element    xpath:${JNC XP NB TOOLBAR}${JNC XP ICON RUN}
