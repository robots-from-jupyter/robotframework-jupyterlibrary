*** Settings ***
Documentation       Keywords for outputs in Jupyter Notebook

Resource            JupyterLibrary/clients/notebook/Selectors.resource


*** Keywords ***
Current Notebook Cell Output Should Contain
    [Documentation]    Check whether the currently-selected cell's output contains the given text
    [Arguments]    ${expected}
    Wait Until Element Contains    css:${JNB CSS ACTIVE OUTPUT}    ${expected}

Screenshot Each Output Of Active Notebook Cell
    [Documentation]    Capture all of the outputs of the current Cell as screenshots
    ...    with a ``prefix``.
    [Arguments]    ${prefix}
    ${outputs} =    Get WebElements    css:${JNB CSS ACTIVE OUTPUT}
    FOR    ${i}    IN RANGE    ${outputs.__len__()}
        Capture Element Screenshot    ${outputs[${i}]}    ${prefix}_output_${i}.png
    END

Screenshot Markdown Of Active Notebook Cell
    [Documentation]    Capture all of the rendered Markdown of the current Document as screenshots
    ...    with a ``prefix``.
    [Arguments]    ${prefix}
    ${inputs} =    Get WebElements    css:${JNB CSS ACTIVE MARKDOWN}
    FOR    ${i}    IN RANGE    ${inputs.__len__()}
        Capture Element Screenshot    ${inputs[${i}]}    ${prefix}_markdown_${i}.png
    END

Screenshot Each Output Of Active Notebook Document
    [Documentation]    Capture all of the outputs of the current **Notebook** as
    ...    screenshots with a ``prefix``.
    [Arguments]    ${prefix}
    ${cells} =    Get WebElements    css:${JNB CSS CELL}
    FOR    ${i}    IN RANGE    ${cells.__len__()}
        Click Element    ${cells[${i}]}
        Run Keyword And Ignore Error    Click Element    ${cells[${i + 1}]}
        Click Element    ${cells[${i}]}
        Sleep    0.1s
        Screenshot Each Output Of Active Notebook Cell    ${prefix}_cell_${i}
        Screenshot Markdown Of Active Notebook Cell    ${prefix}_cell_${i}
    END
