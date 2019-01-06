*** Settings ***
Resource   JupyterLibrary/clients/nteract_on_jupyter/Selectors.robot

*** Keywords ***
Current Notebook Classic Cell Output Should Contain
    [Arguments]  ${expected}
    Wait until Element Contains  css:${JNC CSS ACTIVE OUTPUT}    ${expected}

Screenshot Each Output of Active Notebook Classic Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the outputs of the current Cell as screenshots
    ...   with a ``prefix``.
    ${outputs} =  Get WebElements  css:${JNC CSS ACTIVE OUTPUT SUBAREAS}
    :FOR   ${i}  IN RANGE  ${outputs.__len__()}
    \  Capture Element Screenshot  ${outputs[${i}]}  ${prefix}_output_${i}.png

Screenshot Markdown of Active Notebook Classic Cell
    [Arguments]  ${prefix}
    [Documentation]   Capture all of the rendered Markdown of the current Document as screenshots
    ...   with a ``prefix``.
    ${inputs} =  Get WebElements  css:${JNC CSS ACTIVE MARKDOWN}
    :FOR   ${i}  IN RANGE  ${inputs.__len__()}
    \  Capture Element Screenshot  ${inputs[${i}]}  ${prefix}_markdown_${i}.png

Screenshot Each Output of Active Notebook Classic Document
    [Arguments]  ${prefix}
    [Documentation]  Capture all of the outputs of the current **Notebook** as
    ...   screenshots with a ``prefix``.
    ${cells} =  Get WebElements  css:${JNC CSS CELL}
    :FOR  ${i}   IN RANGE  ${cells.__len__()}
    \   Click element  ${cells[${i}]}
    \   Run Keyword And Ignore Error    Click element  ${cells[${i + 1}]}
    \   Click element  ${cells[${i}]}
    \   Sleep  0.1s
    \   Screenshot Each Output of Active Notebook Classic Cell	${prefix}_cell_${i}
    \   Screenshot Markdown of Active Notebook Classic Cell 	${prefix}_cell_${i}
