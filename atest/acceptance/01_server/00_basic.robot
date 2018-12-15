*** Settings ***
Suite Teardown    Terminate All Jupyter Servers
Force Tags        server
Library           JupyterLibrary
Library           Process
Library           OperatingSystem

*** Test Cases ***
Start one server
    ${nbserver} =    Start New Jupyter Server    stdout=${OUTPUT_DIR}${/}one_server.log    stderr=STDOUT
    ${ready} =    Wait for Jupyter Server to be Ready
    Should be equal as integers    ${ready}    1    msg=One server should be ready
    ${terminated} =    Terminate All Jupyter Servers
    Should be equal as integers    ${terminated}    1    msg=One server should have been terminated
    ${log} =    Get Process Result    ${nbserver}    stderr=${True}
    Should Contain    ${log}    The Jupyter Notebook is running    msg=Log should contain expected status message

Start three servers
    ${nb1} =    Start New Jupyter Server    stdout=${OUTPUT_DIR}${/}one_of_three_server.log    stderr=STDOUT
    ${nb2} =    Start New Jupyter Server    stdout=${OUTPUT_DIR}${/}two_of_three_server.log    stderr=STDOUT
    ${ready} =    Wait for Jupyter Server to be Ready    ${nb2}    ${nb1}
    Should be equal as integers    ${ready}    2    msg=Three servers should be ready
    ${nb3} =    Start New Jupyter Server    stdout=${OUTPUT_DIR}${/}three_of_three_server.log    stderr=STDOUT
    ${terminated} =    Terminate All Jupyter Servers
    Should be equal as integers    ${terminated}    3    msg=Three servers should have been terminated
    ${log1} =    Get Process Result    ${nb1}    stderr=${True}
    Should Contain    ${log1}    The Jupyter Notebook is running    msg=Log should contain expected status message
    ${log2} =    Get Process Result    ${nb2}    stderr=${True}
    Should Contain    ${log2}    The Jupyter Notebook is running    msg=Log should contain expected status message
    ${terminated} =    Terminate All Jupyter Servers
    Should be equal as integers    ${terminated}    0    msg=No servers should have been terminated

Server Files
    [Setup]    Create File    ${OUTPUT_DIR}${/}foo.txt    bar
    ${nb1} =    Start New Jupyter Server    stdout=${OUTPUT_DIR}${/}files.log    stderr=STDOUT
    Copy Files to Jupyter Directory    ${OUTPUT_DIR}${/}*.txt
    ${nbdir} =    Get Jupyter Directory    ${nb1}
    ${out} =    Get File    ${nbdir}${/}foo.txt
    Should Be Equal    ${out}    bar
    Copy Files from Jupyter Directory    foo.txt    ${OUTPUT_DIR}
    Terminate All Jupyter Servers
    ${out} =    Get File    ${OUTPUT_DIR}${/}foo.txt
    Should Be Equal    ${out}    bar
    File Should Not Exist    ${nbdir}${/}foo.txt
    [Teardown]    Remove File    ${OUTPUT_DIR}${/}foo.txt
