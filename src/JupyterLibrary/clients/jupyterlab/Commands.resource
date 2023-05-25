*** Settings ***
Documentation       Command keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource
Resource            JupyterLibrary/clients/jupyterlab/Shortcuts.resource


*** Keywords ***
Execute JupyterLab Command
    [Documentation]    Use the JupyterLab
    ...    [https://jupyterlab.readthedocs.io/en/stable/user/commands.html|Command Palette]
    ...    to run a ``command`` and ``accept`` any resulting dialogs, then ``close``
    ...    the Command Palette.
    [Arguments]    ${command}    ${accept}=${True}    ${close}=${True}
    Maybe Accept A JupyterLab Prompt
    Open Command Palette With Hotkeys
    Input Text    css:${JLAB CSS CMD INPUT}    ${command}
    Wait Until Element Is Visible    css:${JLAB CSS CMD ITEM}
    Click Element    css:${JLAB CSS CMD ITEM}
    Run Keyword If    ${accept}    Maybe Accept A JupyterLab Prompt
    Run Keyword If    ${close}    Maybe Close JupyterLab Sidebar

Open Command Palette With Hotkeys
    [Documentation]
    ...    Open the JupyterLab Command Palette with the platform-specific keyboard
    ...    shortcuts. Note that the JupyterLab 3 modal command palette is flaky.
    ...    Enabling the sidebar-based mechanism may help, see:
    ...    - [#Set JupyterLab Plugin Settings|Set JupyterLab Plugin Settings]
    ${accel} =    Get ACCEL Key
    Press Keys    id:main    ${accel}+SHIFT+c
    Wait Until Element Is Visible    css:${JLAB CSS CMD INPUT}
    Run Keyword And Ignore Error    Click Element    css:${JLAB CSS CMD INPUT}

Reset JupyterLab And Close
    [Documentation]    Try to clean up after doing some things to the JupyterLab
    ...    open in the current browser, then close the browser.
    Execute JupyterLab Command    Reset Application State
    Close Browser

Close All JupyterLab Tabs
    [Documentation]    Attempt to close all the currently-open tabs, accepting any dialogs
    Maybe Accept A JupyterLab Prompt
    Execute JupyterLab Command    Close All Tabs
    Maybe Accept A JupyterLab Prompt
