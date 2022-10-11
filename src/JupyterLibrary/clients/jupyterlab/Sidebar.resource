*** Settings ***
Documentation       Sidebar keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource


*** Keywords ***
Maybe Close JupyterLab Sidebar
    [Documentation]    Attempt to close the JupyterLab sidebar
    ${active} =    Get WebElements    css:${JLAB CSS ACTIVE SIDEBAR}
    Run Keyword If    ${active}    Click Element    ${active[0]}

Maybe Open JupyterLab Sidebar
    [Documentation]    Attempt to open a JupyterLab sidebar with the given ``title``
    ...    (if not already open).
    [Arguments]    ${title}
    Maybe Close JupyterLab Sidebar
    Run Keyword And Ignore Error
    ...    Click Element    css:${JLAB CSS SIDEBAR TAB}\[title^="${title}"]
