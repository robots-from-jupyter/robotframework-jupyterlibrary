*** Settings ***
Documentation       Icon keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/PageInfo.resource


*** Variables ***
&{JLAB1 CSS ICONS}
...                     add=span[data-icon="add"]
...                     run=span[data-icon="run"]
...                     filled circle=.jp-CircleFilledIcon
...                     empty circle=.jp-CircleEmptyIcon
&{JLAB2 CSS ICONS}
...                     add=svg[@data-icon='ui-components:add']
...                     run=svg[@data-icon='ui-components:run']
...                     filled circle=svg[@data-icon='ui-components:circle-filled']
...                     empty circle=svg[@data-icon='ui-components:circle-empty']
&{JLAB1 XP ICONS}
...                     add=span[@data-icon = 'add']
...                     run=span[@data-icon = 'run']
...                     filled circle=div[contains(@class, 'jp-CircleFilledIcon')]
...                     empty circle=div[contains(@class, 'jp-CircleEmptyIcon')]
&{JLAB2 XP ICONS}
...                     add=*[@data-icon='ui-components:add']
...                     run=*[@data-icon='ui-components:run']
...                     filled circle=*[@data-icon='ui-components:circle-filled']
...                     empty circle=*[@data-icon='ui-components:circle-empty']


*** Keywords ***    ***
Get JupyterLab Icon CSS
    [Documentation]    Get a Lab version-specific, but general CSS selector for an ``icon``.
    [Arguments]    ${icon}
    ${version} =    Get JupyterLab Application Version Info
    ${sel} =    Set Variable If    ${version[0].__eq__('1')}
    ...    ${JLAB1 CSS ICONS['${icon}']}
    ...    ${JLAB2 CSS ICONS['${icon}']}
    [Return]    ${sel}

Get JupyterLab Icon XPath
    [Documentation]    Get a Lab version-specific, but general XPath selector for an ``icon``.
    [Arguments]    ${icon}
    ${version} =    Get JupyterLab Application Version Info
    ${sel} =    Set Variable If    ${version[0].__eq__('1')}
    ...    ${JLAB1 XP ICONS['${icon}']}
    ...    ${JLAB2 XP ICONS['${icon}']}
    [Return]    ${sel}
