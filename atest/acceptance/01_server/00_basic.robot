*** Settings ***
Library  JupyterLibrary
Library  Process
Test Teardown  Terminate All Processes

*** Test Cases  ***
Start one server
  ${nbserver} =  Start New Jupyter Server
  ${ready} =  Wait for Jupyter Server to be Ready
  Should be equal as integers  ${ready}  1
  ...  msg=One server should be ready
  ${terminated} =  Terminate All Jupyter Servers
  Should be equal as integers  ${terminated}  1
  ...  msg=One server should have been terminated
  ${log} =  Get Process Result   ${nbserver}  stderr=${True}
  Should Contain    ${log}    The Jupyter Notebook is running
  ...  msg=Log should contain expected status message

Start three servers
  ${nb1} =  Start New Jupyter Server
  ${nb2} =  Start New Jupyter Server
  ${ready} =  Wait for Jupyter Server to be Ready  ${nb2}  ${nb1}
  Should be equal as integers  ${ready}  2
  ...  msg=Three servers should be ready
  ${nb3} =  Start New Jupyter Server
  ${terminated} =  Terminate All Jupyter Servers
  Should be equal as integers  ${terminated}  3
  ...  msg=Three servers should have been terminated
  ${log1} =  Get Process Result   ${nb1}  stderr=${True}
  Should Contain    ${log1}    The Jupyter Notebook is running
  ...  msg=Log should contain expected status message
  ${log2} =  Get Process Result   ${nb2}  stderr=${True}
  Should Contain    ${log2}    The Jupyter Notebook is running
  ...  msg=Log should contain expected status message
  ${log3} =  Get Process Result   ${nb3}  stderr=${True}
  Should Not Contain    ${log3}    The Jupyter Notebook is running
  ...  msg=Unawaited server log should not contain expected status message
  ${terminated} =  Terminate All Jupyter Servers
  Should be equal as integers  ${terminated}  0
  ...  msg=No servers should have been terminated
  Run Keyword And Expect Error    Only 0 of 3*  Wait for Jupyter Server to be Ready  ${nb2}  ${nb1}  ${nb3}
