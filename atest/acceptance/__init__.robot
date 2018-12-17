*** Settings ***
Suite Setup       Set Screenshot Directory    ${OUTPUT_DIR}${/}${OS}${/}${BROWSER}${/}screenshots
Suite Teardown    Clean Up Everything
Force Tags        os:${OS}    browser:${BROWSER}
Library           JupyterLibrary
Library           Process

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Jupyter Servers
    Terminate All Processes
