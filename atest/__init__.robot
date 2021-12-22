*** Settings ***
Library             JupyterLibrary
Library             Process

Suite Setup         Set Screenshot Directory    ${OUTPUT_DIR}${/}${OS}${/}${BROWSER}${/}screenshots
Suite Teardown      Clean Up Everything

Force Tags          os:${os}    browser:${browser}

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Jupyter Servers
    Terminate All Processes
