*** Settings ***
Resource   JupyterLibrary/clients/jupyterlab/Selectors.robot

*** Keywords ***
Launch a new JupyterLab Document
    [Arguments]    ${kernel}=Python 3    ${category}=Notebook
    [Documentation]    Use the JupyterLab launcher to launch a document of ``category``
    ...   Notebook or Console with the given ``kernel``, and wait until the loading
    ...   animation is complete.
    Click Element    xpath:${JLAB XP CARD}\[@title='${kernel}'][@data-category='${category}']
    Run Keyword And Ignore Error    timeout=2s  Wait Until Page Contains Element    css:${JLAB CSS SPINNER}
    Run Keyword And Ignore Error    timeout=5s  Wait Until Page Does Not Contain Element    css:${JLAB CSS SPINNER}
    Wait Until Page Contains Element    css:${JLAB CSS ACTIVE INPUT}
    Sleep    0.5s
