*** Settings ***
Suite Teardown    Clean Up Everything
Library           JupyterLibrary
Library           Process

*** Keywords ***
Clean Up Everything
    Close All Browsers
    Terminate All Jupyter Servers
    Terminate All Processes
