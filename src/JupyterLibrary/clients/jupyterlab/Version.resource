*** Settings ***
Documentation       Overrides for JupyterLab 4


*** Variables ***
${CM6 CSS EDITOR}       .cm-content
${CM6 JS INSTANCE}      .cmView


*** Keywords ***
Update Globals For JupyterLab Version
    [Documentation]    Update global variables for JupyterLab version.
    ${version_info} =    Get JupyterLab Application Version Info
    Run Keyword    Update Globals For JupyterLab ${version_info[0]}

Update Globals For JupyterLab 2
    [Documentation]    Replace current selectors with JupyterLab 4-specific ones.
    Skip    For JupyterLab 2 support, use `robotframework-jupyterlibrary 0.4.x`

Update Globals For JupyterLab 3
    [Documentation]    Replace current selectors with JupyterLab 3-specific ones.
    Log    JupyterLab 3 is now the current version.

Update Globals For JupyterLab 4
    [Documentation]    Replace current selectors with JupyterLab 4-specific ones.
    Set Global Variable    ${CM VERSION}    ${6}
    Set Global Variable    ${CM CSS EDITOR}    ${CM6 CSS EDITOR}
    Set Global Variable    ${CM JS INSTANCE}    ${CM6 JS INSTANCE}
    Set Global Variable    ${JLAB CSS ACTIVE INPUT}    ${JLAB CSS ACTIVE CELL} ${CM CSS EDITOR}
    Log    JupyterLab 4 is now the current version.
