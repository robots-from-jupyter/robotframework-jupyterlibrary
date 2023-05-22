*** Settings ***
Documentation       Page config keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource
Library             String
Library             json    WITH NAME    JSON


*** Variables ***
${JLAB XP PAGEINFO}                 script[contains(@id, 'jupyter-config-data')]
# keep this updated below
@{JLAB DEFAULT PAGEINFO TAGS}       appName    appVersion    buildAvailable
...                                 buildCheck    notebookVersion    devMode


*** Keywords ***
Get JupyterLab Page Info
    [Documentation]    Get one (or all) of the ``pageInfo`` ``key`` s from JupyterLab's HTML ``<head>``.
    ...    Optionally ``clear`` the cached info first.
    ...
    ...    See also:
    ...    - [#Tag With JupyterLab Metadata|Tag With JupyterLab Metadata]
    [Arguments]    ${key}=${EMPTY}    ${clear}=${False}
    ${pageInfo} =    Get Variable Value    ${JLAB PAGEINFO CACHE}    ${EMPTY}
    Run Keyword If    ${clear} or not ${pageInfo.__len__()}    Update JupyterLab PageInfo Cache
    ${pageInfo} =    Set Variable    ${JLAB PAGEINFO CACHE}
    ${result} =    Set Variable If    ${key.__len__()}    ${pageInfo.get("${key}")}    ${pageInfo}
    [Return]    ${result}

Update JupyterLab PageInfo Cache
    [Documentation]    Update the cached JupyterLab ``pageInfo``. _Not usually needed._
    ${sel} =    Set Variable    xpath://${JLAB XP PAGEINFO}
    Wait Until Page Contains Element    ${sel}
    ${txt} =    JupyterLibrary.Get Element Attribute    ${sel}    innerHTML
    ${pageInfo} =    JSON.Loads    ${txt}
    Set Suite Variable    ${JLAB PAGEINFO CACHE}    ${pageInfo}    children=${True}

Tag With JupyterLab Metadata
    [Documentation]    Tag the current test (or suite) with ``keys`` from the
    ...    JupyterLab ``pageInfo``.
    ...    The default ``keys``: ``appName`` ``appVersion`` ``buildAvailable``
    ...    ``buildCheck`` ``notebookVersion`` ``devMode``
    [Arguments]    ${keys}=${JLAB DEFAULT PAGEINFO TAGS}    ${clear}=${False}
    ${info} =    Get JupyterLab Page Info    clear=${clear}
    FOR    ${key}    IN    @{keys}
        ${val} =    Set Variable    ${info.get("${key}")}
        Set Tags    jupyterlab:${key}:${val}
    END

Get JupyterLab Application Version Info
    [Documentation]    Get the version of the application ``2.3.0.rc1`` as a list of
    ...    strings from ``pageInfo``, e.g. ``["2", "3", "1", "rc1"]``. Optionally ``clear``
    ...    the cached info first.
    [Arguments]    ${clear}=${False}
    ${version} =    Get JupyterLab Page Info    appVersion    clear=${clear}
    ${version_info} =    Set Variable    ${version.split(".")}
    [Return]    ${version_info}
