*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot

*** Keywords ***
Current nteract Cell Output Should Contain
  [Arguments]  ${expected}
  Element Should Contain    css:${NOJ CSS ACTIVE CELL OUTPUTS}    ${expected}

Screenshot Each Output of Active nteract Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the outputs of the current Cell as screenshots
    ...   with a ``prefix``.
    ${outputs} =  Get WebElements  css:${NOJ CSS ACTIVE CELL OUTPUTS} > *
    :FOR   ${i}  IN RANGE  ${outputs.__len__()}
    \  Capture Element Screenshot  ${outputs[${i}]}  ${prefix}_output_${i}.png

Screenshot Markdown of Active nteract Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the rendered Markdown of the current Document as screenshots
    ...   with a ``prefix``.
    ${inputs} =  Get WebElements  css:${NOJ CSS ACTIVE CELL MARKDOWN}
    :FOR   ${i}  IN RANGE  ${inputs.__len__()}
    \  Capture Element Screenshot  ${inputs[${i}]}  ${prefix}_markdown_${i}.png

Screenshot Each Output of Active nteract Document
    [Arguments]  ${prefix}
    [Documentation]  Capture all of the outputs of the current **Document** as
    ...   screenshots with a ``prefix``.
    ${cells} =  Get WebElements  css:${NOJ CSS CELL}
    :FOR  ${i}   IN RANGE  ${cells.__len__()}
    \   Click element  ${cells[${i}]}
    \   Run Keyword And Ignore Error    Click element  ${cells[${i + 1}]}
    \   Click element  ${cells[${i}]}
    \   Sleep  0.1s
    \   Screenshot Each Output of Active nteract Cell	${prefix}_cell_${i}
    \   Screenshot Markdown of Active nteract Cell 	${prefix}_cell_${i}
