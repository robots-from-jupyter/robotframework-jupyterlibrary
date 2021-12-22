*** Settings ***
Documentation       Tests of Jupyter Classic client keywords

Library             JupyterLibrary

Suite Setup         Wait For New Jupyter Server To Be Ready
Suite Teardown      Terminate All Jupyter Servers

Force Tags          client:notebook
