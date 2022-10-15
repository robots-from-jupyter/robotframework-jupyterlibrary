*** Settings ***
Documentation       Settings keywords for JupyterLab

Library             OperatingSystem
Resource            JupyterLibrary/clients/jupyterlab/PageInfo.resource


*** Variables ***
${JLAB FILE EXT SETTINGS}       .jupyterlab-settings


*** Keywords ***
Get JupyterLab User Settings Directory
    [Documentation]    Retrieve the user settings directory, which may not yet exist.
    ...    == Note ==
    ...    - Assumes access to the local file system
    ${dir} =    Get JupyterLab Page Info    key=userSettingsDir
    ${dir} =    Normalize Path    ${dir}
    [Return]    ${dir}

Get JupyterLab Plugin Settings File
    [Documentation]    Get the full file path (which may or may not exist) for a plugin's settings.
    ...    The file may be encoded as JSON5.
    ...    ``package`` is the ``package.json`` -compatible name.
    ...    ``plugin`` is the specific name of the settings schema, derived from
    ...    the plugin's ``id``.
    [Arguments]    ${package}    ${plugin}
    ${settings} =    Get JupyterLab User Settings Directory
    ${path} =    Join Path    ${settings}    ${package}    ${plugin}${JLAB FILE EXT SETTINGS}
    [Return]    ${path}

Set JupyterLab Plugin Settings
    [Documentation]
    ...    Overwrite the user's settings for the ``plugin`` in the ``package`` with ``config``.
    ...    ``package`` is the ``package.json`` -compatible name.
    ...    ``plugin`` is the specific name of the settings schema, derived from
    ...    the plugin's ``id``.
    ...
    ...    == Note ==
    ...    - ``config`` will be checked for JSON5 "well-formedness", but no schema
    ...    validation is performed.
    ...    - Assumes access to the local file system
    [Arguments]    ${package}    ${plugin}    &{config}
    ${path} =    Get JupyterLab Plugin Settings File    ${package}    ${plugin}
    ${json} =    Evaluate    __import__("json").dumps(${config})
    Create File    ${path}    ${json}

Get JupyterLab Plugin Settings
    [Documentation]
    ...    Retrieve the user's settings for the ``plugin`` in the ``package`` as a ``dict``.
    ...    ``package`` is the ``package.json`` -compatible name.
    ...    ``plugin`` is the specific name of the settings schema, derived from
    ...    the plugin's ``id``.
    ...
    ...    == Note ==
    ...    - Assumes access to the local file system
    ...    - Can't handle JSON5 "features" like extra commas and comments
    [Arguments]    ${package}    ${plugin}
    ${path} =    Get JupyterLab Plugin Settings File    ${package}    ${plugin}
    ${raw} =    Get File    ${path}
    ${config} =    Evaluate    __import__("json").loads(r"""${raw}""")
    [Return]    ${config}

Disable JupyterLab Modal Command Palette
    [Documentation]    Disable the modal JupyterLab Command Palette. Can help testability.
    Set JupyterLab Plugin Settings    @jupyterlab/apputils-extension    palette
    ...    modal=${FALSE}

Enable JupyterLab Modal Command Palette
    [Documentation]    Enable the modal JupyterLab Command Palette.
    Set JupyterLab Plugin Settings    @jupyterlab/apputils-extension    palette
    ...    modal=${TRUE}
