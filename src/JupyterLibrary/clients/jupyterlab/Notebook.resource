*** Settings ***
Documentation       Notebook keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource
Resource            JupyterLibrary/common/CodeMirror.resource


*** Variables ***
@{HELLO WORLD}      print("hello world")


*** Keywords ***
Add And Run JupyterLab Code Cell
    [Documentation]    Add a ``code`` cell to the ``n`` th notebook on the page and run it.
    ...    ``code`` is a list of strings to set as lines in the code editor.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    [Arguments]    @{code}    ${n}=1
    ${add icon} =    Get JupyterLab Icon XPath    add
    ${nb} =    Get WebElement    xpath://div${JLAB XP NB FRAG}\[${n}]
    # rely on main area widgets all having ids
    ${nbid} =    JupyterLibrary.Get Element Attribute    ${nb}    id
    ${icon} =    Get WebElement Relative To    ${nb}    xpath:div${JLAB XP NB TOOLBAR FRAG}//${add icon}
    Click Element    ${icon}
    Sleep    0.1s
    ${cell} =    Get WebElement Relative To    ${nb}
    ...    css:${JLAB CSS ACTIVE INPUT.replace('''${JLAB CSS ACTIVE DOC}''', '')}
    Click Element    ${cell}
    Set CodeMirror Value    \#${nbid}${JLAB CSS ACTIVE INPUT}    @{code}
    Run Current JupyterLab Code Cell    ${n}
    Click Element    ${cell}

Wait Until JupyterLab Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy, in the ``n`` th notebook.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    [Arguments]    ${n}=1
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
    [Documentation]    Run the currently-selected cell(s) in the ``n`` th notebook.
    ...    ``n`` is the 1-based index of the notebook, usually in order of opening.
    [Arguments]    ${n}=1
    ${run icon} =    Get JupyterLab Icon XPath    run
    ${nb} =    Get WebElement    xpath://div${JLAB XP NB FRAG}\[${n}]
    ${run btn} =    Get WebElement Relative To    ${nb}    xpath:div${JLAB XP NB TOOLBAR FRAG}//${run icon}
    Click Element    ${run btn}
    Sleep    0.5s
