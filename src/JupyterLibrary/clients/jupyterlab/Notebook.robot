*** Settings ***
Resource          JupyterLibrary/clients/jupyterlab/Selectors.robot
Resource          JupyterLibrary/common/CodeMirror.robot

*** Variables ***
@{HELLO WORLD}    print("hello world")

*** Keywords ***
Add and Run JupyterLab Code Cell
    [Arguments]    @{code}
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    ...    ``code`` is a list of strings to set as lines in the code editor
    ${nl} =    Set Variable    \n
    ${add icon} =    Get JupyterLab Icon XPath    add
    Click Element    xpath:${JLAB XP NB TOOLBAR}//${add icon}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JLAB CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JLAB CSS ACTIVE INPUT}    @{code}
    Run Current JupyterLab Code Cell
    Click Element    ${cell}

Wait Until JupyterLab Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    ${busy icon} =    Get JupyterLab Icon XPath    filled circle
    Run Keyword And Ignore Error
    ...    Wait Until Page Does Not Contain Element    xpath://${JLAB XP NB TOOLBAR}//${busy icon}
    Run Keyword And Ignore Error
    ...    Wait Until Page Does Not Contain    xpath:${JLAB XP NB TOOLBAR}//${busy icon}

Save JupyterLab Notebook
    [Documentation]    Use the `Save Notebook` command
    Execute JupyterLab Command    Save Notebook

Run Current JupyterLab Code Cell
    ${run icon} =    Get JupyterLab Icon XPath    run
    ${sel} =    Set Variable    xpath:${JLAB XP NB TOOLBAR}//${run icon}
    Wait Until Page Contains Element    ${sel}
    Click Element    ${sel}
    Sleep    0.5s
