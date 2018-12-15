*** Settings ***
Resource   JupyterLibrary/resources/JupyterLab/Selectors.robot

*** Keywords ***
Add and Run JupyterLab Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    Click Element    css:${JLAB CSS NB TOOLBAR} ${JLAB CSS ICON ADD}
    Sleep    0.1s
    Click Element    css:${JLAB CSS CELL}
    Execute JavaScript    document.querySelector("${JLAB CSS CELL}").CodeMirror.setValue(`${code}`)
    Click Element    css:${JLAB CSS ICON RUN}

Wait Until JupyterLab Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JLAB CSS BUSY KERNEL}
    Wait Until Page Does Not Contain    ${JLAB TEXT BUSY PROMPT}
