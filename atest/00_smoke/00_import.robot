*** Settings ***
Documentation       Very simplest tests of importing

Library             JupyterLibrary


*** Test Cases ***
Just Import
    [Documentation]    Does it import?
    Log    JupyterLibrary probably imported
