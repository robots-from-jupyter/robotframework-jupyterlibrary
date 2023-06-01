*** Settings ***
Documentation       Selectors for Jupyter Notebook 7+
...                 Any `${JLAB*}` variables should be used with caution. and may require
...                 Dedicated keywords (or JSON variables) in the future.

Resource            JupyterLibrary/common/CodeMirror.resource
Resource            JupyterLibrary/common/Lumino.resource
Resource            JupyterLibrary/clients/jupyterlab/Selectors.resource


*** Variables ***
# imports from jupyterlab
${JNB CSS CELL}                         ${JLAB CSS CELL}
${JNB CSS ACCEPT}                       ${JLAB CSS MOD ACCEPT}

# css selectors
${JNB CSS TREE}                         .jp-DirListing
${JNB CSS TREE LIST}                    .jp-DirListing-content
${JNB CSS TREE LIST ITEM}               ${JNB CSS TREE LIST} .jp-DirListing-item
${JNB CSS TREE NEW MENU}                ${LM CSS MENU}
${JNB CSS TREE NEW NOTEBOOK}            ${JNB CSS TREE NEW MENU} li[data-command="notebook:create-new"]
${JNB CSS TREE MENU ITEM LABEL}         ${LM CSS MENU ITEM LABEL}
${JNB CSS KERNEL DIALOG SELECT}         .jp-Dialog select
${JNB CSS NB KERNEL BUSY}               .kernel_budy_icon
${JNB CSS CMD BUTTON}                   button[data-jupyter-action="jupyter-notebook:show-command-palette"]
${JNB CSS CMD PALETTE}                  .modal.cmd-palette.in
${JNB CSS CMD INPUT}                    ${JNB CSS CMD PALETTE}    input[type="search"]
${JNB CSS CMD ITEM}                     ${JNB CSS CMD PALETTE}    .typeahead-result li > a
${JNB CSS ACTIVE CELL}                  ${JLAB CSS ACTIVE CELL}
${JNB CSS ACTIVE INPUT}                 ${JNB CSS ACTIVE CELL} ${CM6 CSS EDITOR}
${JNB CSS ACTIVE OUTPUT}                ${JLAB CSS ACTIVE CELL} ${JLAB CSS OUTPUT CHILD}
${JNB CSS ACTIVE MARKDOWN}              ${JNB CSS ACTIVE CELL} .text_cell_render
${JNB CSS IDLE KERNEL}                  .jp-Notebook-ExecutionIndicator[data-status="idle"]

# xpath selectors
${JNB XP NB TOOLBAR}                    //div${JLAB XP NB TOOLBAR}
${JNB XP TREE TOOLBAR}                  //*[contains(@class, 'jp-FileBrowser-toolbar')]
${JNB XP TREE TOOLBAR ITEM}             ${JNB XP TREE TOOLBAR}//li[contains(@class, 'lm-MenuBar-item')]
${JNB XP TREE TOOLBAR ITEM LABEL}       ${JNB XP TREE TOOLBAR ITEM}//*[contains(@class, 'lm-MenuBar-itemLabel')]
${JNB XP TREE NEW BUTTON}               ${JNB XP TREE TOOLBAR ITEM LABEL}\[text()='New']

# magic text
${JNB TEXT BUSY PROMPT}                 In [*]:
