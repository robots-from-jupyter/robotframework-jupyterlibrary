*** Settings ***
Documentation       Keywords for working with the Jupyter Notebook Clasic web application
...                 You should have already started a Jupyter Server, such as with
...                 *Wait For New Jupyter Server To Be Ready*.

Resource            JupyterLibrary/clients/notebook/Selectors.resource


*** Keywords ***
Open Notebook
    [Documentation]    Open Jupyter Notebook, served from the given (or most-recently-started)
    ...    ``nbserver`` in a ``browser`` (or ``headlessfirefox``) or ``url``,
    ...    then wait for the splash screen.
    ...    Extra ``configuration`` is passed on to SeleniumLibrary's *Open Browser*.
    [Arguments]    ${browser}=headlessfirefox    ${nbserver}=${None}    ${url}=${EMPTY}    &{configuration}
    ${nbserver_url} =    Run Keyword If    not "${url}"    Get Jupyter Server URL    ${nbserver}
    ${token} =    Run Keyword If    not "${url}"    Get Jupyter Server Token    ${nbserver}
    ${final_url} =    Set Variable If    "${url}"    ${url}    ${nbserver_url}tree?token=${token}
    Open Browser    url=${final_url}    browser=${browser}    &{configuration}
    Update Globals For JupyterLab 4
    Wait Until Element Is Visible    css:${JNB CSS TREE}
    Wait Until Element Is Visible    css:${JNB CSS TREE LIST}    timeout=10s

Launch A New Notebook
    [Documentation]    Use the Jupyter Notebook tree to launch a Notebook with the
    ...    given ``kernel``
    [Arguments]    ${kernel}=Python 3 (ipykernel)
    Click Element    xpath:${JNB XP TREE NEW BUTTON}
    Wait Until Element Is Visible    css:${JNB CSS TREE NEW MENU}
    Mouse Over    css:${JNB CSS TREE NEW NOTEBOOK}
    Click Element    css:${JNB CSS TREE NEW NOTEBOOK} ${JNB CSS TREE MENU ITEM LABEL}
    Switch Window    NEW
    Wait Until Element Is Visible    css:${JNB CSS KERNEL DIALOG SELECT}
    Select From List By Label    css:${JNB CSS KERNEL DIALOG SELECT}    ${kernel}
    Click Element    css:${JNB CSS ACCEPT}
    Wait Until Element Is Visible    css:${JNB CSS IDLE KERNEL}    timeout=30s
