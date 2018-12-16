*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot

*** Keywords ***
Current Notebook Classic Cell Output Should Contain
  [Arguments]  ${expected}
  Element Should Contain    css:${JNC CSS ACTIVE OUTPUT}    ${expected}
