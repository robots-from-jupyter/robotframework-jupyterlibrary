*** Settings ***
Resource   JupyterLibrary/clients/jupyterlab/Selectors.robot

*** Keywords ***
Maybe Close JupyterLab Sidebar
    [Documentation]  Attempt to close the JupyterLab sidebar
    ${active} =  Get WebElements  css:${JLAB CSS ACTIVE SIDEBAR}
    Run Keyword If  ${active}   Click Element    ${active[0]}

Maybe Open JupyterLab Sidebar
    [Arguments]  ${title}
    [Documentation]  Attempt to open a JupyterLab sidebar with the given ``title``
    ...   (if not already open).
    Maybe Close JupyterLab Sidebar
    Click Element  css:${JLAB CSS SIDEBAR TAB}\[title^="${title}"]
