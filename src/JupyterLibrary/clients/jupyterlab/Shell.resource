*** Settings ***
Documentation       Application shell keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource
Resource            JupyterLibrary/clients/jupyterlab/PageInfo.resource
Resource            JupyterLibrary/clients/jupyterlab/Version.resource


*** Keywords ***
# robocop: disable=too-many-arguments

Open JupyterLab
    [Documentation]    Open JupyterLab, served from the given (or most-recently-started)
    ...    ``nbserver`` in a ``browser`` (or ``headlessfirefox``) or ``url``,
    ...    then wait for the splash screen.
    ...    Extra ``configuration`` is passed on to SeleniumLibrary's [#Open Browser|Open Browser].
    [Arguments]    ${browser}=headlessfirefox
    ...    ${nbserver}=${None}
    ...    ${url}=${EMPTY}
    ...    ${clear}=${False}
    ...    ${pageinfo tags}=@{JLAB DEFAULT PAGEINFO TAGS}
    ...    &{configuration}
    ${nbserver_url} =    Run Keyword If    not "${url}"    Get Jupyter Server URL    ${nbserver}
    ${token} =    Run Keyword If    not "${url}"    Get Jupyter Server Token    ${nbserver}
    ${final_url} =    Set Variable If    "${url}"    ${url}    ${nbserver_url}lab?token=${token}
    Open Browser    url=${final_url}    browser=${browser}    &{configuration}
    Maybe Wait For JupyterLab Splash Screen
    Tag With JupyterLab Metadata    ${pageinfo tags}    clear=${clear}
    LOG    ${JLAB CSS ACTIVE INPUT}
    Update Globals For JupyterLab Version
    LOG    ${JLAB CSS ACTIVE INPUT}

Wait For JupyterLab Splash Screen
    [Documentation]    Wait for the JupyterLab splash animation, waiting ``timeout``
    ...    for the splash screen to appear/disappear, then ``sleep``.
    [Arguments]    ${timeout}=10s    ${sleep}=2s
    Wait Until Element Is Visible    css:#${JLAB ID SPLASH}    timeout=${timeout}
    Wait Until Page Does Not Contain Element    css:#${JLAB ID SPLASH}    timeout=${timeout}
    Sleep    ${sleep}

Maybe Wait For JupyterLab Splash Screen
    [Documentation]    Wait for the JupyterLab splash animation, waiting ``timeout``
    ...    for the splash screen to appear/disappear, then ``sleep``. Ignore errors.
    [Arguments]    ${timeout}=10s    ${sleep}=2s
    Run Keyword And Ignore Error    Wait For JupyterLab Splash Screen    ${timeout}    ${sleep}

Click JupyterLab Menu
    [Documentation]    Click a top-level JupyterLab menu bar item by ``label``,
    ...    e.g. _File_, _Help_, etc.
    [Arguments]    ${label}
    ${xpath} =    Set Variable    ${JLAB XP TOP}${JLAB XP MENU LABEL}\[text() = '${label}']
    Wait Until Element Is Visible    ${xpath}
    Mouse Over    ${xpath}
    Click Element    ${xpath}
    Run Keyword And Ignore Error    Mouse Over    ${xpath}

Click JupyterLab Menu Item
    [Documentation]    Click a currently-visible JupyterLab menu item by ``label``.
    [Arguments]    ${label}
    ${item} =    Set Variable    ${JLAB XP MENU ITEM LABEL VISIBLE}\[text() = '${label}']
    Wait Until Element Is Visible    ${item}
    Mouse Over    ${item}
    Click Element    ${item}
    Run Keyword And Ignore Error    Mouse Over    ${item}

Open With JupyterLab Menu
    [Documentation]    Click into a ``menu``, then a series of ``submenus``.
    [Arguments]    ${menu}    @{submenus}
    Click JupyterLab Menu    ${menu}
    FOR    ${submenu}    IN    @{submenus}
        Click JupyterLab Menu Item    ${submenu}
    END

Maybe Accept A JupyterLab Prompt
    [Documentation]    Click the accept button in a JupyterLab dialog (if one is open).
    ${accept} =    Get WebElements    css:${JLAB CSS ACCEPT}
    Run Keyword If    ${accept}    Click Element    ${accept[0]}

Get JupyterLab Dock Panel Tab
    [Documentation]    Get the ``n`` -th JupyterLab Dock Panel Tab with ``label`` as a ``WebElement``.
    ...    ``n`` is the 1-based index of the like- ``label`` ed tabs.
    [Arguments]    ${label}    ${n}=1
    ${els} =    Get WebElements    xpath:${JLAB XP DOCK TAB LABEL}\[. = '${label}']/..
    [Return]    ${els[${n}-1]}

Close JupyterLab Dock Panel Tab
    [Documentation]    Close the ``n`` -th JupyterLab Dock Panel Tab with ``label`` as a ``WebElement``.
    ...    ``n`` is the 1-based index of the like- ``label`` ed tabs.
    [Arguments]    ${label}    ${n}=1
    ${tab} =    Get JupyterLab Dock Panel Tab    ${label}    ${n}
    ${last div} =    Get WebElement Relative To    ${tab}    xpath:./div[last()]
    Click Element    ${last div}
