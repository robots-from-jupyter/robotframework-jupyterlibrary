*** Variables ***
${JLAB ID SPLASH}      jupyterlab-splash

${JLAB CSS CELL}       .jp-Notebook .jp-Cell:last-of-type .jp-InputArea-editor .CodeMirror
${JLAB CSS SPINNER}        .jp-Spinner
${JLAB CSS CMD PALETTE}    li[data-id="command-palette"]
${JLAB CSS CMD INPUT}    .p-CommandPalette-input
${JLAB CSS CMD ITEM}    .p-CommandPalette-item
${JLAB CSS ACCEPT}  .jp-mod-accept
${JLAB CSS ACTIVE SIDEBAR}  .jp-SideBar .p-TabBar-tab.p-mod-current
${JLAB CSS SIDEBAR TAB}  .jp-SideBar .p-TabBar-tab
${JLAB CSS BUSY KERNEL}  .jp-Toolbar-kernelStatus.jp-FilledCircleIcon

${JLAB CSS NB TOOLBAR}  .jp-NotebookPanel-toolbar

${JLAB CSS ICON RUN}  .jp-RunIcon
${JLAB CSS ICON ADD}  .jp-AddIcon

${JLAB XP TOP}            //div[@id='jp-top-panel']
${JLAB XP MENU LABEL}       //div[@class='p-MenuBar-itemLabel']
${JLAB XP MENU ITEM LABEL}  //div[@class='p-Menu-itemLabel']
${JLAB XP CARD}           //div[@class='jp-LauncherCard']
${JLAB XP DOCK}           //div[@id='jp-main-dock-panel']

${JLAB TEXT BUSY PROMPT}  In [*]:
