*** Settings ***
Documentation     Interact with the RobotLab ne JupyterLab application shell
Resource   JupyterLibrary/resources/jupyterlab/Selectors.robot


*** Keywords ***
Maybe Close JupyterLab Sidebar
    [Documentation]  Attempt to close the JupyterLab sidebar
    ${active} =  Get WebElements  css:${JLAB CSS ACTIVE SIDEBAR}
    Run Keyword If  ${active}   Click Element    ${active[0]}

Maybe Open JupyterLab Sidebar
    [Arguments]  ${data id}
    [Documentation]  Attempt to open a JupyterLab sidebar (if not already open)
    Maybe Close JupyterLab Sidebar
    ${sel} =  Catenate   SEPARATOR=${EMPTY}   ${JLAB CSS SIDEBAR TAB}  [data-id="${data id}"]
    Click Element  css:${sel}
