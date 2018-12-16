*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot

*** Keywords ***
Current nteract Cell Output Should Contain
  [Arguments]  ${expected}
  Element Should Contain    css:${NOJ CSS ACTIVE CELL OUTPUTS}    ${expected}
