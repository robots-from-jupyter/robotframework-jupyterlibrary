*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot
Resource   JupyterLibrary/common/CodeMirror.robot

*** Keywords ***
Add and Run nteract Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    ${creators} =  Get WebElements    css:${NOJ CSS CREATOR}
    Hide nteract Status Bar
    Scroll To End Of Page
    Scroll Element Into View  ${creators[-1]}
    Click Element  ${creators[-1]}
    Click Element    css:${NOJ CSS CREATOR}:hover ${NOJ CSS ADD CODE CELL}
    ${cells} =  Get WebElements    css:${NOJ CSS CELL INPUT}
    Scroll To End Of Page
    Mouse Over  ${cells[-1]}
    Click Element    ${cells[-1]}
    Show nteract Status Bar
    Set CodeMirror Value  ${NOJ CSS ACTIVE CELL INPUT}  ${code}
    Run Current nteract Code Cell

Run Current nteract Code Cell
    Mouse Over    css:${NOJ CSS EXECUTE}
    Click Element    css:${NOJ CSS EXECUTE}

Wait Until nteract Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain    ${NOJ TEXT BUSY PROMPT}

Hide nteract Status Bar
    [Arguments]  ${pointerevents}=
    Execute JavaScript
    ...   document.querySelector("${NOJ CSS STATUS BAR}").style.display = "none"

Show nteract Status Bar
    [Arguments]  ${pointerevents}=
    Execute JavaScript
    ...   document.querySelector("${NOJ CSS STATUS BAR}").style.display = null

Scroll To End Of Page
    Execute JavaScript
    ...   document.querySelector("body").scrollTop = 999999

Scroll To Top Of Page
    Execute JavaScript
    ...   document.querySelector("body").scrollTop = 0

Click nteract Menu
    [Arguments]    ${label}
    [Documentation]    Click a top-level nteract menu bar item with by ``label``,
    ...   e.g. File, Help, etc.
    Scroll To Top Of Page
    ${xpath} =  Set Variable  ${NOJ XP MENU}\[@title = '${label}']
    Wait Until Page Contains Element    ${xpath}
    Mouse Over    ${xpath}

Click nteract Menu Item
    [Arguments]    ${label}
    [Documentation]    Click a currently-visible nteract menu item by ``label``.
    ${item} =    Set Variable  ${NOJ XP MENU ITEM}\[contains(text(), '${label}')]
    Wait Until Page Contains Element    ${item}
    Click Element    ${item}

Open With nteract Menu
    [Arguments]  ${menu}  @{submenus}
    [Documentation]  Click into a ``menu``, then a series of ``submenus``
    Click nteract Menu  ${menu}
    :FOR  ${submenu}  IN  @{submenus}
    \  Click nteract Menu Item  ${submenu}

Save nteract Notebook
    Open With nteract Menu  File  Save
