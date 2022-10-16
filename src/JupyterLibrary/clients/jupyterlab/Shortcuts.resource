*** Settings ***
Documentation       Keyboard shortcut keywords for JupyterLab

Library             platform    WITH NAME    PLATFORM


*** Keywords ***
Get ACCEL Key
    [Documentation]    Get the platform-specific "accelerator key" used for shortcuts:
    ...    - ``Ctrl`` on Linux/Windows
    ...    - ``Cmd`` on MacOS
    ${accel} =    Get Variable Value    ${ACCEL}    ${EMPTY}
    Run Keyword If    not "${accel}"    Update ACCEL Key
    [Return]    ${ACCEL KEY}

Update ACCEL Key
    [Documentation]    Cache the "accelerator key"
    ${system} =    PLATFORM.System
    ${accel} =    Evaluate    "COMMAND" if "${system}" == "Darwin" else "CTRL"
    Set Global Variable    ${ACCEL KEY}    ${accel}
