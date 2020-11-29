*** Settings ***
#
# Example pageInfo
#
#                 <script id="jupyter-config-data" type="application/json">{
#                 "appName": "JupyterLab", "appNamespace": "jupyterlab",
#                 "appSettingsDir": "$PREFIX/share/jupyter/lab/settings", "appUrl": "/lab",
#                 "appVersion": "2.2.9", "asset_url": "", "baseUrl": "/",
#                 "buildAvailable": true, "buildCheck": true, "cacheFiles": true,
#                 "devMode": false, "exposeAppInBrowser": false, "fullAppUrl": "/lab",
#                 "fullListingsUrl": "/lab/api/listings",
#                 "fullMathjaxUrl": "/static/components/MathJax/MathJax.js",
#                 "fullSettingsUrl": "/lab/api/settings", "fullStaticUrl": "/static/lab",
#                 "fullThemesUrl": "/lab/api/themes", "fullTreeUrl": "/lab/tree",
#                 "fullWorkspacesApiUrl": "/lab/api/workspaces", "fullWorkspacesUrl": "/lab/workspaces",
#                 "ga_code": "", "ignorePlugins": [], "listingsUrl": "/lab/api/listings",
#                 "mathjaxConfig": "TeX-AMS-MML_HTMLorMML-full,Safe", "notebookVersion": "[6, 1, 5]",
#                 "quitButton": true, "schemasDir": "$PREFIX/share/jupyter/lab/schemas",
#                 "serverRoot": "$CWD", "settingsUrl": "/lab/api/settings",
#                 "staticDir": "$PREFIX/share/jupyter/lab/static",
#                 "staticUrl": "/static/lab", "store_id": 2,
#                 "templatesDir": "$PREFIX/share/jupyter/lab/static", "terminalsAvailable": true,
#                 "themesDir": "$PREFIX/share/jupyter/lab/themes", "themesUrl": "/lab/api/themes",
#                 "token": "$TOKEN", "treeUrl": "/lab/tree",
#                 "userSettingsDir": "$HOME/.jupyter/lab/user-settings",
#                 "workspacesApiUrl": "/lab/api/workspaces",
#                 "workspacesDir": "$HOME/.jupyter/lab/workspaces",
#                 "workspacesUrl": "/lab/workspaces", "wsUrl": ""
#                 }</script>
#
# **NOTE**: Some pageInfo values might contain $SENSITIVE_INFORMATION.
#                 It is not recommended to store/emit/log pageInfo, unfiltered.
#
Resource          JupyterLibrary/clients/jupyterlab/Selectors.robot
Library           json    WITH NAME    JSON
Library           String

*** Variables ***
# TODO: test with jlab1
${JLAB XP PAGEINFO}    script[contains(@id, 'jupyter-config-data')]
@{JLAB DEFAULT PAGEINFO TAGS}    appName    appVersion    buildAvailable
...               buildCheck    notebookVersion    devMode

*** Keywords ***
Get JupyterLab Page Info
    [Arguments]    ${key}=${EMPTY}    ${clear}=${False}
    [Documentation]    Get one (or all) of the pageConfig datum from JupyterLab's HTML
    ...    See also:
    ...    - *Tag With JupyterLab Metadata*
    ${pageInfo} =    Get Variable Value    ${JLAB PAGEINFO CACHE}    ${EMPTY}
    Run Keyword If    ${clear} or not ${pageInfo.__len__()}    Update JupyterLab PageInfo Cache
    ${pageInfo} =    Set Variable    ${JLAB PAGEINFO CACHE}
    ${result} =    Set Variable If    ${key.__len__()}    ${pageInfo.get(key)}    ${pageInfo}
    [Return]    ${result}

Update JupyterLab PageInfo Cache
    ${sel} =    Set Variable    xpath://${JLAB XP PAGEINFO}
    Wait Until Page Contains Element    ${sel}
    ${txt} =    Get Element Attribute    ${sel}    innerHTML
    ${pageInfo} =    JSON.Loads    ${txt}
    Set Suite Variable    ${JLAB PAGEINFO CACHE}    ${pageInfo}    children=${True}

Tag With JupyterLab Metadata
    [Arguments]    ${keys}=${JLAB DEFAULT PAGEINFO TAGS}    ${clear}=${False}
    [Documentation]    Tag the current test (or suite) with JupyterLab pageInfo
    ${info} =    Get JupyterLab Page Info    clear=${clear}
    FOR    ${key}    IN    @{keys}
        ${val} =    Set Variable    ${info.get("${key}")}
        Set Tags    jupyterlab:${key}:${val}
    END

Get JupyterLab Application Version Info
    [Arguments]    ${clear}=${False}
    ${json} =    Get JupyterLab Page Info    clear=${clear}
    [Return]    ${json['appVersion'].split(".")}
