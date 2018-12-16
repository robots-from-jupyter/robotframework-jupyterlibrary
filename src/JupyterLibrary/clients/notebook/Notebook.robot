*** Settings ***
Resource   JupyterLibrary/clients/notebook/Selectors.robot

*** Keywords ***
Add and Run Notebook Classic Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    Click Element    css:${JNC CSS NB TOOLBAR} ${JNC CSS ICON ADD}
    Sleep    0.1s
    Click Element    css:${JNC CSS CELL}
    Execute JavaScript    document.querySelector("${JNC CSS CELL}").CodeMirror.setValue(`${code}`)
    Click Element    css:${JNC CSS NB TOOLBAR} ${JNC CSS ICON RUN}

Wait Until Notebook Classic Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JNC CSS NB KERNEL BUSY}
    Wait Until Page Does Not Contain    ${JNC TEXT BUSY PROMPT}
