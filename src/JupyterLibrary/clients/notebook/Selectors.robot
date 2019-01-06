*** Variables ***
${JNC CSS TREE LIST}  \#notebook_list
${JNC CSS TREE LIST ITEM}  ${JNC CSS TREE LIST} .list_item
${JNC CSS TREE NEW BUTTON}  \#new-dropdown-button
${JNC CSS TREE NEW MENU}  \#new-menu
${JNC CSS NB KERNEL ICON}  \#kernel_indicator_icon
${JNC CSS NB KERNEL IDLE}  .kernel_idle_icon
${JNC CSS NB KERNEL BUSY}  .kernel_budy_icon
${JNC TEXT BUSY PROMPT}  In [*]:

${JNC CSS CMD BUTTON}  button[data-jupyter-action="jupyter-notebook:show-command-palette"]
${JNC CSS CMD PALETTE}  .modal.cmd-palette.in
${JNC CSS CMD INPUT}  ${JNC CSS CMD PALETTE}  input[type="search"]
${JNC CSS CMD ITEM}  ${JNC CSS CMD PALETTE}  .typeahead-result li > a

${JNC CSS NB TOOLBAR}  \#maintoolbar-container

${JNC CSS ICON ADD}  .fa-plus
${JNC CSS ICON RUN}  .fa-step-forward

${JNC CSS CELL}   \#notebook-container .cell
${JNC CSS ACTIVE CELL}  ${JNC CSS CELL}.selected
${JNC CSS ACTIVE INPUT}  ${JNC CSS ACTIVE CELL} .CodeMirror
${JNC CSS ACTIVE OUTPUT}  ${JNC CSS ACTIVE CELL} .output_wrapper
${JNC CSS ACTIVE OUTPUT SUBAREAS}  ${JNC CSS ACTIVE OUTPUT} .output_subarea
${JNC CSS ACTIVE MARKDOWN}  ${JNC CSS ACTIVE CELL} .text_cell_render
