*** Settings ***
Documentation       Verify Notebook activities in Lab

Library             Process
Library             JupyterLibrary

Suite Teardown      Run Keyword And Ignore Error    Close All Browsers
Test Setup          Open JupyterLab    ${BROWSER}
Test Teardown       Run Keyword And Ignore Error    Reset JupyterLab And Close

Default Tags        notebook


*** Test Cases ***
IPython Notebook on Lab
    [Documentation]    Ensure an IPython Notebook works in Lab.
    Launch A New JupyterLab Document
    Add And Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Current JupyterLab Cell Output Should Contain    hello world
    Capture Page Screenshot    lab${/}10-00-ipython.png
    Save JupyterLab Notebook

IPython Notebook Outputs on Lab
    [Documentation]    Ensure IPython outputs work in Lab.
    Launch A New JupyterLab Document
    FOR    ${i}    IN RANGE    ${10}
        Add And Run JupyterLab Code Cell    print("${i} hello world " * ${i ** 2})
    END
    Wait Until JupyterLab Kernel Is Idle
    Screenshot Each Output Of Active JupyterLab Document    10-10-outputs
    Save JupyterLab Notebook

Multiple Notebooks on Lab
    [Documentation]    Verify two notebooks work
    [Tags]    notebooks
    Disable JupyterLab Modal Command Palette
    ${tab0} =    Make The First Notebook
    ${tab1} =    Make The Second Notebook
    Click Element    ${tab1}
    Drag And Drop By Offset    ${tab1}    800    500
    Capture Page Screenshot    lab${/}10-21-two-notesbook.png
    Close JupyterLab Dock Panel Tab    Untitled1.ipynb
    Maybe Accept A JupyterLab Prompt
    Page Should Not Contain    yet another world


*** Keywords ***
Make The First Notebook
    [Documentation]    Make a simple notebook
    Launch A New JupyterLab Document
    Wait Until JupyterLab Kernel Is Idle
    Add And Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Page Should Contain    hello world
    Capture Page Screenshot    lab${/}10-20-one-notebook.png
    ${tab} =    Get JupyterLab Dock Panel Tab    Untitled.ipynb
    [Return]    ${tab}

Make The Second Notebook
    [Documentation]    Make a another simple notebook
    Launch A New JupyterLab Document
    Add And Run JupyterLab Code Cell    print("yet another world")    n=2
    Wait Until JupyterLab Kernel Is Idle
    Page Should Contain    another world
    ${tab} =    Get JupyterLab Dock Panel Tab    Untitled1.ipynb
    [Return]    ${tab}
