*** Settings ***
Documentation     Interact with the JupyterLab Launcher
Resource   JupyterLibrary/resources/jupyterlab/Selectors.robot

*** Keywords ***
Launch a new JupyterLab Document
    [Arguments]    ${kernel}=Python 3    ${category}=Notebook
    [Documentation]    Use the JupyterLab launcher to launch Notebook or Console
    Click Element    xpath:${JLAB XP CARD}[@title='${kernel}'][@data-category='${category}']
    Wait Until Page Does Not Contain Element    css:${JLAB CSS SPINNER}
    Wait Until Page Contains Element    css:${JLAB CSS CELL}
    Sleep    0.1s
