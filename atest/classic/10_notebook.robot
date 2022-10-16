*** Settings ***
Documentation       Basic tests of notebook in Classic

Library             Process
Library             JupyterLibrary

Test Teardown       Close All Browsers

Default Tags        notebook


*** Test Cases ***
IPython Notebook On Classic
    [Documentation]    Do a notebook work correctly on Classic?
    Open Notebook Classic    ${BROWSER}
    Launch A New Notebook Classic Notebook
    Add And Run Notebook Classic Code Cell    print("hello world")
    Wait Until Notebook Classic Kernel Is Idle
    Current Notebook Classic Cell Output Should Contain    hello world
    Capture Page Screenshot    classic${/}ipython.png

IPython Notebook Outputs On Classic
    [Documentation]    Do outputs work correctly on Classic?
    Open Notebook Classic    ${BROWSER}
    Launch A New Notebook Classic Notebook
    FOR    ${i}    IN RANGE    ${10}
        Add And Run Notebook Classic Code Cell    print("${i} hello world " * ${i ** 2})
    END
    Wait Until Notebook Classic Kernel Is Idle
    Screenshot Each Output Of Active Notebook Classic Document    classic${/}ipython_outputs${/}
