*** Settings ***
Resource   JupyterLibrary/clients/notebook/Selectors.robot
Documentation   Keywords for working with the Jupyter Notebook Clasic web application
...    You should have already started a Jupyter Server, such as with
...    *Wait For New Jupyter Server To Be Ready*.

*** Keywords ***
Open Notebook Classic
    [Arguments]    ${browser}=headlessfirefox  ${nbserver}=${None}  ${url}=${EMPTY}   &{configuration}
    [Documentation]    Open Jupyter Notebook Classic, served from the given (or most-recently-started)
    ...   ``nbserver`` in a ``browser`` (or ``headlessfirefox``) or ``url``,
    ...   then wait for the splash screen.
    ...   Extra ``configuration`` is passed on to SeleniumLibrary's *Open Browser*.
    ${nbserver_url} =  Run Keyword If    not "${url}"  Get Jupyter Server URL  ${nbserver}
    ${token} =  Run Keyword If    not "${url}"  Get Jupyter Server Token  ${nbserver}
    ${final_url} =  Set Variable If   "${url}"   ${url}  ${nbserver_url}tree?token=${token}
    Open Browser    url=${final_url}    browser=${browser}  &{configuration}
    Wait Until Page Contains Element  css:${JNC CSS TREE LIST ITEM}

Launch a new Notebook Classic Notebook
    [Arguments]    ${kernel}=Python 3
    [Documentation]    Use the Jupyter Notebook Classic tree to launch a
    ...   Notebook with the given ``kernel``
    Click Element    css:${JNC CSS TREE NEW BUTTON}
    Wait Until Page Contains Element    css:${JNC CSS TREE NEW MENU}
    Click Element   css:${JNC CSS TREE NEW MENU} a[title$="${kernel}"]
    Select Window   NEW
    Wait Until Page Contains Element  css:${JNC CSS NB KERNEL ICON}${JNC CSS NB KERNEL IDLE}
