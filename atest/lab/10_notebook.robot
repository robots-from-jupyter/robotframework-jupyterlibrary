*** Settings ***
Suite Teardown    Run Keyword and Ignore Error    Close All Browsers
Test Teardown     Run Keyword and Ignore Error    Reset JupyterLab and Close
Default Tags      notebook
Library           JupyterLibrary
Library           Process
Test Setup        Open JupyterLab    ${BROWSER}

*** Test Cases ***
IPython Notebook on Lab
    Launch a new JupyterLab Document
    Add and Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Current JupyterLab Cell Output Should Contain    hello world
    Capture Page Screenshot    10-00-ipython.png
    Save JupyterLab Notebook

IPython Notebook Outputs on Lab
    Launch a new JupyterLab Document
    FOR    ${i}    IN RANGE    ${10}
        Add and Run JupyterLab Code Cell    print("${i} hello world " * ${i ** 2})
    END
    Wait Until JupyterLab Kernel Is Idle
    Screenshot Each Output of Active JupyterLab Document    10-10-outputs
    Save JupyterLab Notebook

Multiple Notebooks on Lab
    [Tags]    notebooks
    Disable JupyterLab Modal Command Palette
    Launch a new JupyterLab Document
    Wait Until JupyterLab Kernel Is Idle
    Add and Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Page Should Contain    hello world
    Capture Page Screenshot    10-20-one-notebook.png
    Launch a new JupyterLab Document
    ${tab1} =    Get JupyterLab Dock Panel Tab    Untitled1.ipynb
    Click Element    ${tab1}
    Add and Run JupyterLab Code Cell    print("yet another world")    n=2
    Wait Until JupyterLab Kernel Is Idle
    Page Should Contain    another world
    Drag And Drop By Offset    ${tab1}    800    500
    Capture Page Screenshot    10-21-two-notesbook.png
    Close JupyterLab Dock Panel Tab    Untitled1.ipynb
    Maybe Accept a JupyterLab Prompt
    Page Should Not Contain    yet another world
