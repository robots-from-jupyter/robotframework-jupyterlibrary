*** Settings ***
Documentation       Common selectors for JupyterLab elements

Resource            JupyterLibrary/common/CodeMirror.resource


*** Variables ***
# robocop: disable=line-too-long
# css selectors
${JLAB CSS ACCEPT}                      .jp-mod-accept
${JLAB CSS ACTIVE DOC}                  .jp-Document:not(.jp-mod-hidden)
${JLAB CSS ACTIVE DOC CELLS}            ${JLAB CSS ACTIVE DOC} .jp-Cell
${JLAB CSS ACTIVE CELL}                 ${JLAB CSS ACTIVE DOC} .jp-Cell.jp-mod-active
${JLAB CSS ACTIVE INPUT}                ${JLAB CSS ACTIVE CELL} .CodeMirror
${JLAB CSS ACTIVE OUTPUT CHILDREN}      ${JLAB CSS ACTIVE CELL} .jp-OutputArea-child
${JLAB CSS OUTPUT}                      .jp-OutputArea-output
${JLAB CSS ACTIVE CELL MARKDOWN}        ${JLAB CSS ACTIVE CELL} .jp-MarkdownOutput:not(.jp-mod-hidden)
${JLAB CSS ACTIVE SIDEBAR}              .jp-SideBar .lm-TabBar-tab.lm-mod-current
${JLAB CSS BUSY KERNEL}                 .jp-Toolbar-kernelStatus.jp-FilledCircleIcon
${JLAB CSS CMD INPUT}                   .lm-CommandPalette-input
${JLAB CSS CMD ITEM}                    .lm-CommandPalette-item
${JLAB CSS NB TOOLBAR}                  .jp-NotebookPanel-toolbar
${JLAB CSS SIDEBAR TAB}                 .jp-SideBar .lm-TabBar-tab
${JLAB CSS SPINNER}                     .jp-Spinner
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
