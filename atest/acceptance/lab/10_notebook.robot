*** Settings ***
Suite Teardown    Run Keyword and Ignore Error    Close All Browsers
Test Teardown     Run Keyword and Ignore Error    Reset JupyterLab and Close
Default Tags      notebook
Library           JupyterLibrary
Library           Process

*** Test Cases ***
IPython Notebook on Lab
    Open JupyterLab    ${BROWSER}
    Launch a new JupyterLab Document
    Add and Run JupyterLab Code Cell    print("hello world")
    Wait Until JupyterLab Kernel Is Idle
    Current JupyterLab Cell Output Should Contain    hello world
    Capture Page Screenshot    lab${/}ipython.png
    Save JupyterLab Notebook

IPython Notebook Outputs on Lab
    Open JupyterLab    ${BROWSER}
    Launch a new JupyterLab Document
    FOR    ${i}    IN RANGE    ${10}
        Add and Run JupyterLab Code Cell    print("${i} hello world " * ${i ** 2})
    END
    Wait Until JupyterLab Kernel Is Idle
    Screenshot Each Output of Active JupyterLab Document    lab${/}ipython_outputs${/}
    Save JupyterLab Notebook
