*** Variables ***
${NOJ CSS TREE LIST}  .listing-root
${NOJ CSS CARD}  .new-notebook
${NOJ CSS CARD KERNEL}  ${NOJ CSS CARD} .display-name-long
${NOJ CSS CELLS}  .cells
${NOJ CSS CELL}  .cell
${NOJ CSS CELL INPUT}  .cell .CodeMirror .CodeMirror
${NOJ CSS ACTIVE CELL}  .focused.cell
${NOJ CSS ACTIVE CELL INPUT}  .focused${NOJ CSS CELL INPUT}
${NOJ CSS ACTIVE CELL OUTPUTS}  .cell.focused .outputs
${NOJ CSS CREATOR}  .creator-hover-region
${NOJ CSS ADD CODE CELL}  .add-code-cell
${NOJ CSS CELL TOOLBAR}  .cell .cell-toolbar
${NOJ CSS EXECUTE}  .focused${NOJ CSS CELL TOOLBAR} .executeButton
${NOJ TEXT BUSY PROMPT}  [*]
${NOJ CSS ACTIVE CELL MARKDOWN}    ${NOJ CSS ACTIVE CELL} > div > .outputs
${NOJ CSS STATUS BAR}  \#root > .status-bar

${NOJ XP MENU}  //div[contains(@class, 'rc-menu-submenu-title')]
${NOJ XP MENU ITEM}  //li[contains(@class, 'rc-menu-item')]
