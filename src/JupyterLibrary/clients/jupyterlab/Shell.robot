*** Settings ***
Resource   JupyterLibrary/clients/jupyterlab/Selectors.robot
Documentation   Keywords for working with the JupyterLab web application
...    You should have already started a Jupyter Server, such as with
...    *Wait For New Jupyter Server To Be Ready*.

*** Keywords ***
Open JupyterLab
    [Arguments]    ${browser}=headlessfirefox  ${nbserver}=${None}  ${url}=${EMPTY}   &{configuration}
    [Documentation]    Open JupyterLab, served from the given (or most-recently-started)
    ...   ``nbserver`` in a ``browser`` (or ``headlessfirefox``) or ``url``,
    ...   then wait for the splash screen.
    ...   Extra ``configuration`` is passed on to SeleniumLibrary's *Open Browser*.
    ${nbserver_url} =  Run Keyword If    not "${url}"  Get Jupyter Server URL  ${nbserver}
    ${token} =  Run Keyword If    not "${url}"  Get Jupyter Server Token  ${nbserver}
    ${final_url} =  Set Variable If   "${url}"   ${url}  ${nbserver_url}lab?token=${token}
    Open Browser    url=${final_url}    browser=${browser}  &{configuration}
    Wait for JupyterLab Splash Screen

Wait for JupyterLab Splash Screen
    [Documentation]    Wait for the JupyterLab splash animation
    Wait Until Page Contains Element    ${JLAB ID SPLASH}
    Wait Until Page Does Not Contain Element    ${JLAB ID SPLASH}    timeout=10s
    Sleep    0.1s

Click JupyterLab Menu
    [Arguments]    ${label}
    [Documentation]    Click a top-level JupyterLab menu bar item with by ``label``,
    ...   e.g. File, Help, etc.
    ${xpath} =  Set Variable  ${JLAB XP TOP}${JLAB XP MENU LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${xpath}
    Mouse Over    ${xpath}
    Click Element    ${xpath}

Click JupyterLab Menu Item
    [Arguments]    ${label}
    [Documentation]    Click a currently-visible JupyterLab menu item by ``label``.
    ${item} =    Set Variable  ${JLAB XP MENU ITEM LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${item}
    Mouse Over    ${item}
    Click Element    ${item}

Open With JupyterLab Menu
    [Arguments]  ${menu}  @{submenus}
    [Documentation]  Click into a ``menu``, then a series of ``submenus``
    Click JupyterLab Menu  ${menu}
    :FOR  ${submenu}  IN  @{submenus}
    \  Click JupyterLab Menu Item  ${submenu}

Maybe Accept a JupyterLab Prompt
    [Documentation]  Click the accept button in a JupyterLab dialog (if one is open).
    ${accept} =  Get WebElements  css:${JLAB CSS ACCEPT}
    Run Keyword If  ${accept}   Click Element    ${accept[0]}
