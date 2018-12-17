*** Variables ***
${JLAB CSS ACCEPT}  .jp-mod-accept
${JLAB CSS ACTIVE DOC}  .jp-Document:not(.jp-mod-hidden)
${JLAB CSS ACTIVE DOC CELLS}  ${JLAB CSS ACTIVE DOC} .jp-Cell
${JLAB CSS ACTIVE CELL}  ${JLAB CSS ACTIVE DOC} .jp-Cell.jp-mod-active
${JLAB CSS ACTIVE INPUT}  ${JLAB CSS ACTIVE CELL} .CodeMirror
${JLAB CSS ACTIVE OUTPUT CHILDREN}    ${JLAB CSS ACTIVE CELL} .jp-OutputArea-child
${JLAB CSS OUTPUT}   .jp-OutputArea-output
${JLAB CSS ACTIVE CELL MARKDOWN}    ${JLAB CSS ACTIVE CELL} .jp-MarkdownOutput:not(.jp-mod-hidden)

${JLAB CSS ACTIVE SIDEBAR}  .jp-SideBar .p-TabBar-tab.p-mod-current
${JLAB CSS BUSY KERNEL}  .jp-Toolbar-kernelStatus.jp-FilledCircleIcon
${JLAB CSS CMD INPUT}    .p-CommandPalette-input
${JLAB CSS CMD ITEM}    .p-CommandPalette-item
${JLAB CSS ICON ADD}  .jp-AddIcon
${JLAB CSS ICON RUN}  .jp-RunIcon
${JLAB CSS NB TOOLBAR}  .jp-NotebookPanel-toolbar
${JLAB CSS SIDEBAR TAB}  .jp-SideBar .p-TabBar-tab
${JLAB CSS SPINNER}        .jp-Spinner
${JLAB ID SPLASH}      jupyterlab-splash
${JLAB TEXT BUSY PROMPT}  In [*]:
${JLAB XP CARD}           //div[@class='jp-LauncherCard']
${JLAB XP DOCK}           //div[@id='jp-main-dock-panel']
${JLAB XP MENU ITEM LABEL}  //div[@class='p-Menu-itemLabel']
${JLAB XP MENU LABEL}       //div[@class='p-MenuBar-itemLabel']
${JLAB XP TOP}            //div[@id='jp-top-panel']
