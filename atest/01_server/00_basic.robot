*** Settings ***
Documentation       Verify Jupyter server basics

Library             Process
Library             OperatingSystem
Library             JupyterLibrary

Suite Setup         Create Directory    ${LOGS}
Suite Teardown      Terminate All Jupyter Servers

Force Tags          server


*** Variables ***
${LOGS}     ${OUTPUT_DIR}${/}${OS}${/}${BROWSER}${/}logs${/}


*** Test Cases ***
Start one server
    [Documentation]    Can we manage a single server?
    ${nbserver} =    Start New Jupyter Server    stdout=${LOGS}1.log    stderr=STDOUT
    ${ready} =    Wait For Jupyter Server To Be Ready
    ${url} =    Get Jupyter Server URL
    Should Be Equal As Integers    ${ready}    1    msg=One server should be ready
    ${terminated} =    Terminate All Jupyter Servers
    Should Be Equal As Integers    ${terminated}    1    msg=One server should have been terminated
    ${log} =    Get Process Result    ${nbserver}    stderr=${True}
    Should Contain    ${log}    ${url}    msg=Log should contain expected status message

Start three servers
    [Documentation]    Can we manage multiple servers?
    [Setup]    Create Directory    ${LOGS}3
    ${nb1}    ${url1} =    Start A Server    1
    ${nb2}    ${url2} =    Start A Server    2
    ${ready} =    Wait For Jupyter Server To Be Ready    ${nb2}    ${nb1}
    Should Be Equal As Integers    ${ready}    2    msg=Two servers should be ready
    ${nb3}    ${url3} =    Start A Server    3
    ${terminated} =    Terminate All Jupyter Servers
    Should Be Equal As Integers    ${terminated}    3    msg=Three servers should have been terminated
    Check A Server Process Log    ${nb1}    ${url1}
    ${terminated} =    Terminate All Jupyter Servers
    Should Be Equal As Integers    ${terminated}    0    msg=No servers should have been terminated

Server Files
    [Documentation]    Can we interact with files the server can see?
    [Setup]    Create File    ${OUTPUT_DIR}${/}foo.txt    bar
    ${nb1} =    Start New Jupyter Server    stdout=${LOGS}files.log    stderr=STDOUT
    Copy Files To Jupyter Directory    ${OUTPUT_DIR}${/}*.txt
    ${nbdir} =    Get Jupyter Directory    ${nb1}
    ${out} =    Get File    ${nbdir}${/}foo.txt
    Should Be Equal    ${out}    bar
    Copy Files From Jupyter Directory    foo.txt    ${OUTPUT_DIR}
    Terminate All Jupyter Servers
    ${out} =    Get File    ${OUTPUT_DIR}${/}foo.txt
    Should Be Equal    ${out}    bar
    File Should Not Exist    ${nbdir}${/}foo.txt
    [Teardown]    Remove File    ${OUTPUT_DIR}${/}foo.txt


*** Keywords ***
Start A Server
    [Documentation]    Start an indexed server.
    [Arguments]    ${idx}
    ${proc} =    Start New Jupyter Server    stdout=${LOGS}3${/}${idx}.log    stderr=STDOUT
    ${url} =    Get Jupyter Server URL    ${proc}
    [Return]    ${proc}    ${url}

Check A Server Process Log
    [Documentation]    Verify a process log contains the expected value.
    [Arguments]    ${proc}    ${expected}
    ${log} =    Get Process Result    ${proc}    stderr=${True}
    Should Contain    ${log}    ${expected}    msg=Log should contain expected status message
