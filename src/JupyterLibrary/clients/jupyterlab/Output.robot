*** Settings ***
Resource   JupyterLibrary/clients/jupyterlab/Selectors.robot

*** Keywords ***
Current JupyterLab Cell Output Should Contain
  [Arguments]  ${expected}
  Wait Until Page Contains Element  css:${JLAB CSS ACTIVE OUTPUT CHILDREN}
  Element Should Contain    css:${JLAB CSS ACTIVE OUTPUT CHILDREN}    ${expected}

Screenshot Each Output of Active JupyterLab Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the outputs of the current Cell as screenshots
    ...   with a ``prefix``.
    ${outputs} =  Get WebElements  css:${JLAB CSS ACTIVE OUTPUT CHILDREN} ${JLAB CSS OUTPUT} > *
    :FOR   ${i}  IN RANGE  ${outputs.__len__()}
    \  Capture Element Screenshot  ${outputs[${i}]}  ${prefix}_output_${i}.png

Screenshot Markdown of Active JupyterLab Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the rendered Markdown of the current Document as screenshots
    ...   with a ``prefix``.
    ${inputs} =  Get WebElements  css:${JLAB CSS ACTIVE CELL MARKDOWN}
    :FOR   ${i}  IN RANGE  ${inputs.__len__()}
    \  Capture Element Screenshot  ${inputs[${i}]}  ${prefix}_markdown_${i}.png

Screenshot Each Output of Active JupyterLab Document
    [Arguments]  ${prefix}
    [Documentation]  Capture all of the outputs of the current **Document** as
    ...   screenshots with a ``prefix``.
    ${cells} =  Get WebElements  css:${JLAB CSS ACTIVE DOC CELLS}
    :FOR  ${i}   IN RANGE  ${cells.__len__()}
    \   Click element  ${cells[${i}]}
    \   Run Keyword And Ignore Error    Click element  ${cells[${i + 1}]}
    \   Click element  ${cells[${i}]}
    \   Sleep  0.1s
    \   Screenshot Each Output of Active JupyterLab Cell	${prefix}_cell_${i}
    \   Screenshot Markdown of Active JupyterLab Cell 	${prefix}_cell_${i}
