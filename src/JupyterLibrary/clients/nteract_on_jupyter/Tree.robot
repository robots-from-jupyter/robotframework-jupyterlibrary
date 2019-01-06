*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot
Documentation   Keywords for working with nteract web application
...    You should have already started a Jupyter Server, such as with
...    *Wait For New Jupyter Server To Be Ready*.

*** Keywords ***
Open nteract
    [Arguments]    ${browser}=headlessfirefox  ${nbserver}=${None}  ${url}=${EMPTY}   &{configuration}
    [Documentation]    Open nteract, served from the given (or most-recently-started)
    ...   ``nbserver`` in a ``browser`` (or ``headlessfirefox``) or ``url``,
    ...   then wait for the splash screen.
    ...   Extra ``configuration`` is passed on to SeleniumLibrary's *Open Browser*.
    ${nbserver_url} =  Run Keyword If    not "${url}"  Get Jupyter Server URL  ${nbserver}
    ${token} =  Run Keyword If    not "${url}"  Get Jupyter Server Token  ${nbserver}
    ${final_url} =  Set Variable If   "${url}"   ${url}  ${nbserver_url}nteract?token=${token}
    Open Browser    url=${final_url}    browser=${browser}  &{configuration}
    Wait Until Page Contains Element  css:${NOJ CSS TREE LIST}
    Sleep  1s

Launch a new nteract Notebook
    [Arguments]    ${kernel}=Python 3
    [Documentation]    Use the nteract tree to launch a
    ...   Notebook with the given ``kernel``
    Click Element   css:${NOJ CSS CARD KERNEL}\[title$="${kernel}"]
    Sleep  1s
    Run Keyword and Ignore Error  Select Window   NEW
    Wait Until Page Contains Element  css:${NOJ CSS CELL}
