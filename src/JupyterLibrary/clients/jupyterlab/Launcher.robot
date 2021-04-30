*** Settings ***
Resource          JupyterLibrary/clients/jupyterlab/Selectors.robot

*** Keywords ***
Launch a new JupyterLab Document
    [Arguments]    ${kernel}=Python 3    ${category}=Notebook    ${timeout}=10s    ${sleep}=0.5s
    [Documentation]    Use the JupyterLab launcher to launch a document of ``category``
    ...    Notebook or Console with the given ``kernel``, and wait until the loading
    ...    animation is complete.
    ${launcher} =    Get WebElements    xpath:${JLAB XP LAUNCHER}
    Run Keyword If    not ${launcher.__len__()}    Execute JupyterLab Command    New Launcher
    Wait Until Page Contains Element    xpath:${JLAB XP CARD}    timeout=${timeout}
    Click Element    xpath:${JLAB XP CARD}\[@title='${kernel}'][@data-category='${category}']
    Run Keyword And Ignore Error
    ...    Wait Until Page Contains Element    css:${JLAB CSS SPINNER}
    Run Keyword And Ignore Error
    ...    Wait Until Page Does Not Contain Element    css:${JLAB CSS SPINNER}
    Wait Until Page Contains Element    css:${JLAB CSS ACTIVE INPUT}
    Sleep    ${sleep}
