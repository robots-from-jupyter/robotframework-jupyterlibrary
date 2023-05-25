*** Settings ***
Documentation       Basic tests of Notebook activity in Jupyter Notebook

Library             Process
Library             JupyterLibrary

Test Teardown       Close All Browsers

Default Tags        activity:notebook


*** Test Cases ***
IPython Notebook On Notebook
    [Documentation]    Do a notebook work correctly on Notebook?
    Open Notebook    ${BROWSER}
    Launch A New Notebook
    Add And Run Notebook Code Cell    print("hello world")
    Wait Until Notebook Kernel Is Idle
    Current Notebook Cell Output Should Contain    hello world
    Capture Page Screenshot    notebook${/}ipython.png

IPython Notebook Outputs On Notebook
    [Documentation]    Do outputs work correctly on Notebook?
    Open Notebook    ${BROWSER}
    Launch A New Notebook
    FOR    ${i}    IN RANGE    ${10}
        Add And Run Notebook Code Cell    print("${i} hello world " * ${i ** 2})
    END
    Wait Until Notebook Kernel Is Idle
    Screenshot Each Output Of Active Notebook Document    notebook${/}ipython_outputs${/}
