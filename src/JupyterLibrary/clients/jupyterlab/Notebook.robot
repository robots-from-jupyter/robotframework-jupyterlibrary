*** Settings ***
Resource          JupyterLibrary/clients/jupyterlab/Selectors.robot
Resource          JupyterLibrary/common/CodeMirror.robot

*** Variables ***
@{HELLO WORLD}    print("hello world")

*** Keywords ***
Add and Run JupyterLab Code Cell
    [Arguments]    @{code}    ${n}=1
    [Documentation]    Add a ``code`` cell to the ``n`` th notebook on the page and run it.
    ...    ``code`` is a list of strings to set as lines in the code editor.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    ${nl} =    Set Variable    \n
    ${add icon} =    Get JupyterLab Icon XPath    add
    Click Element    xpath://div${JLAB XP NB FRAG}\[${n}]//div${JLAB XP NB TOOLBAR FRAG}//${add icon}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JLAB CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JLAB CSS ACTIVE INPUT}    @{code}
    Run Current JupyterLab Code Cell
    Click Element    ${cell}

Wait Until JupyterLab Kernel Is Idle
    [Arguments]    ${n}=1
    [Documentation]    Wait for a kernel to be busy, and then stop being busy, in the ``n`` th notebook.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    ${busy icon} =    Get JupyterLab Icon XPath    filled circle
    ${sel} =    Set Variable
    ...    xpath://div${JLAB XP NB FRAG}\[${n}]//div${JLAB XP NB TOOLBAR FRAG}//${busy icon}
    Run Keyword And Ignore Error
    ...    Wait Until Page Does Not Contain Element    ${sel}
    Run Keyword And Ignore Error
    ...    Wait Until Page Does Not Contain    ${sel}

Save JupyterLab Notebook
    [Documentation]    Use the `Save Notebook` command with the currently-active notebook.
    Execute JupyterLab Command    Save Notebook

Run Current JupyterLab Code Cell
    [Arguments]    ${n}=1
    [Documentation]    Run the currently-selected cell(s) in the ``n`` th notebook.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    ${run icon} =    Get JupyterLab Icon XPath    run
    ${sel} =    Set Variable
    ...    xpath://div${JLAB XP NB FRAG}\[${n}]//div${JLAB XP NB TOOLBAR FRAG}//${run icon}
    Wait Until Page Contains Element    ${sel}
    Click Element    ${sel}
    Sleep    0.5s
