*** Settings ***
Library           platform    WITH NAME    PLATFORM

*** Keywords ***
Get ACCEL key
    [Documentation]    Get the "accelerator key" used for shortcuts
    ${accel} =    Get Variable Value    ${ACCEL}    ${EMPTY}
    Run Keyword If    not "${accel}"    Update ACCEL Key
    [Return]    ${ACCEL KEY}

Update ACCEL Key
    [Documentation]    Cache the "accelerator key"
    ${system} =    PLATFORM.system
    ${accel} =    Evaluate    "COMMAND" if "${system}" == "Darwin" else "CTRL"
    Set Global Variable    ${ACCEL KEY}    ${accel}
