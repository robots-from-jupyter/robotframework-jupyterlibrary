*** Settings ***
Documentation       Tests of JupyterLibrary in different clients

Library             Process
Library             JupyterLibrary

Suite Setup         Set Screenshot Directory    ${OUTPUT_DIR}${/}${OS}${/}${BROWSER}${/}screenshots
Suite Teardown      Clean Up Everything

Force Tags          os:${os}    browser:${browser}


*** Keywords ***
Clean Up Everything
    [Documentation]    Attempt to gracefully stop all Jupyter servers and browsers
    Close All Browsers
    Terminate All Jupyter Servers
    Terminate All Processes
