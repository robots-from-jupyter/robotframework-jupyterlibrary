*** Settings ***
Documentation       Common selectors for JupyterLab elements

Resource            JupyterLibrary/common/CodeMirror.resource
Resource            JupyterLibrary/common/Lumino.resource


*** Variables ***
# robocop: disable=line-too-long
# top-level mod utility classes
${JLAB CSS MOD ACTIVE}                  .jp-mod-active
${JLAB CSS MOD ACCEPT}                  .jp-mod-accept
${JLAB CSS MOD HIDDEN}                  .jp-mod-hidden

# deprecated
${JLAB CSS ACCEPT}                      ${JLAB CSS MOD ACCEPT}    # deprecated

# css atom element selectors
${JLAB CSS CELL}                        .jp-Cell
${JLAB CSS OUTPUT MARKDOWN}             .jp-MarkdownOutput

# app and utility
${JLAB CSS DOC}                         .jp-Document
${JLAB CSS SIDEBAR}                     .jp-SideBar
${JLAB CSS SPINNER}                     .jp-Spinner

# component selectors
${JLAB CSS NB TOOLBAR}                  .jp-NotebookPanel-toolbar
${JLAB CSS OUTPUT}                      .jp-OutputArea-output
${JLAB CSS OUTPUT CHILD}                .jp-OutputArea-child

# compounds
${JLAB CSS ACTIVE DOC}                  ${JLAB CSS DOC}:not(${JLAB CSS MOD HIDDEN})
${JLAB CSS ACTIVE DOC CELLS}            ${JLAB CSS ACTIVE DOC} ${JLAB CSS CELL}
${JLAB CSS ACTIVE CELL}                 ${JLAB CSS ACTIVE DOC} ${JLAB CSS CELL}${JLAB CSS MOD ACTIVE}
${JLAB CSS ACTIVE OUTPUT CHILDREN}      ${JLAB CSS ACTIVE CELL} ${JLAB CSS OUTPUT CHILD}
${JLAB CSS ACTIVE CELL MARKDOWN}        ${JLAB CSS ACTIVE CELL} ${JLAB CSS OUTPUT MARKDOWN}:not(${JLAB CSS MOD HIDDEN})
${JLAB CSS ACTIVE SIDEBAR}              ${JLAB CSS SIDEBAR} ${LM CSS TAB}${LM CSS MOD CURRENT}
${JLAB CSS BUSY KERNEL}                 .jp-Toolbar-kernelStatus.jp-FilledCircleIcon
${JLAB CSS CMD INPUT}                   ${LM CSS CMD INPUT}
${JLAB CSS CMD ITEM}                    ${LM CSS CMD ITEM}
${JLAB CSS SIDEBAR TAB}                 ${JLAB CSS SIDEBAR} ${LM CSS TAB}

# overloaded by version
${JLAB CSS ACTIVE INPUT}                ${JLAB CSS ACTIVE CELL} .CodeMirror

# magic ids
${JLAB ID SPLASH}                       jupyterlab-splash
# magic strings
${JLAB TEXT BUSY PROMPT}                In [*]:
# xpath selectors
${JLAB XP LAUNCHER}                     //div[contains(@class, 'jp-Launcher-body')]
${JLAB XP CARD}                         //div[contains(@class, 'jp-LauncherCard')]
${JLAB XP DOCK}                         //div[@id='jp-main-dock-panel']
${JLAB XP MENU ITEM}                    //li[contains(@class, 'lm-Menu-item')]
${JLAB XP MENU ITEM LABEL}              //div[contains(@class, 'lm-Menu-itemLabel')]
${JLAB XP MENU ITEM VISIBLE}            ${JLAB XP MENU ITEM}\[not(contains(@class,'lm-mod-hidden'))]
${JLAB XP MENU ITEM LABEL VISIBLE}      ${JLAB XP MENU ITEM VISIBLE}/div[contains(@class, 'lm-Menu-itemLabel')]
${JLAB XP MENU LABEL}                   //div[contains(@class, 'lm-MenuBar-itemLabel')]
${JLAB XP TOP}                          //div[@id='jp-top-panel']
${JLAB XP MAIN AREA FRAG}               [contains(@class, 'jp-MainAreaWidget')]
${JLAB XP NB FRAG}                      ${JLAB XP MAIN AREA FRAG}\[contains(@class, 'jp-NotebookPanel')]
${JLAB XP NB TOOLBAR FRAG}              [contains(@class, 'jp-NotebookPanel-toolbar')]
${JLAB XP NB TOOLBAR}                   //div${JLAB XP NB TOOLBAR FRAG}
${JLAB XP BUSY KERNEL}
...                                     //*[local-name() = 'div' and contains(@class, 'jp-FilledCircleIcon' or (local-name() = 'svg' and contains(@data-icon, 'ui-components:circle-filled')))]
# dock panel
${JLAB XP DOCK PANEL}                   //*[@id = 'jp-main-dock-panel']
${JLAB XP DOCK TAB}
...                                     ${JLAB XP DOCK PANEL}//ul[contains(@class, 'lm-TabBar-content')]/li[contains(@class, 'lm-TabBar-tab')]
${JLAB XP DOCK TAB LABEL}               ${JLAB XP DOCK TAB}/div[contains(@class, 'lm-TabBar-tabLabel')]
