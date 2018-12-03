*** Settings ***
Documentation     Interact with the JupyterLab application shell
Resource   JupyterLibrary/resources/jupyterlab/Selectors.robot


*** Keywords ***
Open JupyterLab
    [Arguments]    ${browser}=headlessfirefox  ${nbserver}=${None}
    [Documentation]    Open JupyterLab in a Browser
    ${info} =  Get Jupyter Server Info  ${nbserver}
    Open Browser    ${info['url']}lab?token=${info['token']}    ${browser}
    Wait for JupyterLab Splash Screen

Wait for JupyterLab Splash Screen
    [Documentation]    Wait for the JupyterLab splash animation to run its course
    Wait Until Page Contains Element    ${JLAB ID SPLASH}
    Wait Until Page Does Not Contain Element    ${JLAB ID SPLASH}    timeout=10s
    Sleep    0.1s

Click JupyterLab Menu
    [Arguments]    ${menu_label}
    [Documentation]    Click a top-level JupyterLab Menu bar, e.g. File, Help, etc.
    ${xpath} =  Set Variable  ${JLAB XP TOP}${JLAB XP MENU LABEL}[text() = '${menu_label}']
    Wait Until Page Contains Element    ${xpath}
    Mouse Over    ${xpath}
    Click Element    ${xpath}

Click JupyterLab Menu Item
    [Arguments]    ${item_label}
    [Documentation]    Click a top-level JupyterLab Menu Item (not File, Help, etc.)
    ${item} =    Set Variable    ${JLAB XP MENU ITEM LABEL}[text() = '${item_label}']
    Wait Until Page Contains Element    ${item}
    Mouse Over    ${item}
    Click Element    ${item}

Open With JupyterLab Menu
    [Arguments]  ${menu_label}  @{submenu_labels}
    Click JupyterLab Menu  ${menu_label}
    :FOR  ${item_label}  IN  @{submenu_labels}
    \  Click JupyterLab Menu Item  ${item_label}

Maybe Accept a JupyterLab Prompt
    ${accept} =  Get WebElements  css:${JLAB CSS ACCEPT}
    Run Keyword If  ${accept}   Click Element    ${accept[0]}
