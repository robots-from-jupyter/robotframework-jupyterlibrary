*** Settings ***
Documentation       Notebook keywords for Jupyter Notebook

Resource            JupyterLibrary/clients/notebook/Selectors.resource
Resource            JupyterLibrary/common/CodeMirror.resource


*** Keywords ***
Add And Run Notebook Code Cell
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    [Arguments]    ${code}=print("hello world")
    ${add icon} =    Get JupyterLab Icon XPath    add
    Click Element    xpath:${JNB XP NB TOOLBAR}//${add icon}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JNB CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JNB CSS ACTIVE INPUT}    ${code}
    Run Current Notebook Code Cell
    Click Element    ${cell}

Wait Until Notebook Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JNB CSS NB KERNEL BUSY}
    Wait Until Page Does Not Contain    ${JNB TEXT BUSY PROMPT}

Run Current Notebook Code Cell
    [Documentation]    Run the currently-selected code cell
    ${run icon} =    Get JupyterLab Icon XPath    run
    Click Element    xpath:${JNB XP NB TOOLBAR}//${run icon}
