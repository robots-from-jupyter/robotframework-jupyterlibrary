*** Settings ***
Documentation       Keywords for outputs in Jupyter Classic

Resource            JupyterLibrary/clients/classic/Selectors.resource


*** Keywords ***
Current Notebook Classic Cell Output Should Contain
    [Documentation]    Check whether the currently-selected cell's output contains the given text
    [Arguments]    ${expected}
    Wait Until Element Contains    css:${JNC CSS ACTIVE OUTPUT}    ${expected}

Screenshot Each Output Of Active Notebook Classic Cell
    [Documentation]    Capture all of the outputs of the current Cell as screenshots
    ...    with a ``prefix``.
    [Arguments]    ${prefix}
    ${outputs} =    Get WebElements    css:${JNC CSS ACTIVE OUTPUT SUBAREAS}
    FOR    ${i}    IN RANGE    ${outputs.__len__()}
        Capture Element Screenshot    ${outputs[${i}]}    ${prefix}_output_${i}.png
    END

Screenshot Markdown Of Active Notebook Classic Cell
    [Documentation]    Capture all of the rendered Markdown of the current Document as screenshots
    ...    with a ``prefix``.
    [Arguments]    ${prefix}
    ${inputs} =    Get WebElements    css:${JNC CSS ACTIVE MARKDOWN}
    FOR    ${i}    IN RANGE    ${inputs.__len__()}
        Capture Element Screenshot    ${inputs[${i}]}    ${prefix}_markdown_${i}.png
    END

Screenshot Each Output Of Active Notebook Classic Document
    [Documentation]    Capture all of the outputs of the current **Notebook** as
    ...    screenshots with a ``prefix``.
    [Arguments]    ${prefix}
    ${cells} =    Get WebElements    css:${JNC CSS CELL}
    FOR    ${i}    IN RANGE    ${cells.__len__()}
        Click Element    ${cells[${i}]}
        Run Keyword And Ignore Error    Click Element    ${cells[${i + 1}]}
        Click Element    ${cells[${i}]}
        Sleep    0.1s
        Screenshot Each Output Of Active Notebook Classic Cell    ${prefix}_cell_${i}
        Screenshot Markdown Of Active Notebook Classic Cell    ${prefix}_cell_${i}
    END
