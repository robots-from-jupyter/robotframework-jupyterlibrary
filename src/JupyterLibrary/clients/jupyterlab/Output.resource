*** Settings ***
Documentation       Output keywords for JupyterLab

Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource

*** Keywords ***
Current JupyterLab Cell Output Should Contain
    [Documentation]    Check the current active Notebook cell for the ``expected`` text.
    [Arguments]    ${expected}
    Wait Until Page Contains Element    css:${JLAB CSS ACTIVE OUTPUT CHILDREN}
    Element Should Contain    css:${JLAB CSS ACTIVE OUTPUT CHILDREN}    ${expected}

Screenshot Each Output Of Active JupyterLab Cell
    [Documentation]    Capture all of the outputs of the current _Cell_ as screenshots
    ...    with a ``prefix`` (may include folders).
    [Arguments]    ${prefix}
    ${outputs} =    Get WebElements    css:${JLAB CSS ACTIVE OUTPUT CHILDREN} ${JLAB CSS OUTPUT} > *
    FOR    ${i}    IN RANGE    ${outputs.__len__()}
        Capture Element Screenshot    ${outputs[${i}]}    ${prefix}_output_${i}.png
    END

Screenshot Markdown Of Active JupyterLab Cell
    [Documentation]    Capture all of the rendered Markdown of the current _Document_ as screenshots
    ...    with a ``prefix`` (may include folders).
    [Arguments]    ${prefix}
    ${inputs} =    Get WebElements    css:${JLAB CSS ACTIVE CELL MARKDOWN}
    FOR    ${i}    IN RANGE    ${inputs.__len__()}
        Capture Element Screenshot    ${inputs[${i}]}    ${prefix}_markdown_${i}.png
    END

Screenshot Each Output Of Active JupyterLab Document
    [Documentation]    Capture all of the outputs of the current _Document_ as
    ...    screenshots with a ``prefix`` (may include folders).
    [Arguments]    ${prefix}
    ${cells} =    Get WebElements    css:${JLAB CSS ACTIVE DOC CELLS}
    FOR    ${i}    IN RANGE    ${cells.__len__()}
        Click Element    ${cells[${i}]}
        Run Keyword And Ignore Error    Click Element    ${cells[${i + 1}]}
        Click Element    ${cells[${i}]}
        Sleep    0.1s
        Screenshot Each Output Of Active JupyterLab Cell    ${prefix}_cell_${i}
        Screenshot Markdown Of Active JupyterLab Cell    ${prefix}_cell_${i}
    END

Wait Until JupyterLab Code Cell Is Idle
  [Documentation]  Waits until the given cell in a specific JL tab no longer has an active prompt "[*]:".
  ...              The cell index starts from 1 and you must count empty and markdown cells too.
  [Arguments]  ${tab_id_to_wait}  ${cell_n}  ${timeout}=30
  Wait Until Element Is Not Visible  xpath=//div[@aria-labelledby="${tab_id_to_wait}"]/${JLAB XP NOTEBOOK CONTENT}/div[${cell_n}]/${JLAB XP CELL INPUT STATUS ICON}   ${timeout}

Get A JupyterLab Code Cell Output In a Given Tab
   [Documentation]  It returns the output of a given cell in a specific JL tab.
   ...              The cell index starts from 1 and you must count empty and markdown cells too.
   [Arguments]  ${tab_id_to_read}  ${cell_n}
   ${output_children}=  Get Web Elements  xpath=//div[@aria-labelledby="${tab_id_to_read}"]/${JLAB XP NOTEBOOK CONTENT}/div[${cell_n}]/${JLAB XP CELL OUTPUT GENERIC}
   [Return]  ${output_children}