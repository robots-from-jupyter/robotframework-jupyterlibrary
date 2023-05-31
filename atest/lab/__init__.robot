*** Settings ***
Documentation       Tests of JupyterLab client keywords

Library             Collections
Library             JupyterLibrary

Suite Setup         Set Up JupyterLab Suite
Suite Teardown      Tear Down JupyterLab Suite

Force Tags          client:jupyterlab


*** Variables ***
${DOT_LOCAL_PATH}       .local
${SHARE_PATH}           ${DOT_LOCAL_PATH}${/}share${/}jupyter
${KERNELS_PATH}         ${SHARE_PATH}${/}kernels


*** Keywords ***
Set Up JupyterLab Suite
    [Documentation]    Get ready to test JupyterLab with a server.
    ...    Use well-known environment variables and paths for kernel coverage.
    ${home_dir} =    Set Variable    ${OUTPUT_DIR}${/}.home
    Initialize Coverage Kernel    ${home_dir}
    Wait For New Jupyter Server To Be Ready    jupyter-lab
    ...    env:HOME=${home_dir}
    ...    env:JUPYTER_PREFER_ENV_PATH=0
    ...    stdout=${OUTPUT_DIR}${/}server.log

Tear Down JupyterLab Suite
    [Documentation]    Clean up after JupyterLab
    Run Keyword And Ignore Error
    ...    Execute JupyterLab Command    Shut Down All Kernels
    Terminate All Jupyter Servers

Initialize Coverage Kernel
    [Documentation]    Copy and patch the env's kernel to run under coverage.
    [Arguments]    ${home_dir}
    ${kernels_dir} =    Set Variable    ${home_dir}${/}${KERNELS_PATH}
    Create Directory    ${kernels_dir}
    ${spec_dir} =    Set Variable    ${kernels_dir}${/}python3
    Copy Directory    %{CONDA_PREFIX}${/}share${/}jupyter${/}kernels${/}python3    ${spec_dir}
    ${spec_path} =    Set Variable    ${spec_dir}${/}kernel.json
    ${spec_text} =    Get File    ${spec_path}
    ${spec_json} =    Loads    ${spec_text}
    ${cov_path} =    Set Variable    ${OUTPUT_DIR}${/}coverage
    Create Directory    ${cov_path}
    ${rest} =    Get Slice From List    ${spec_json["argv"]}    1
    ${argv} =    Create List
    ...    ${spec_json["argv"][0]}
    ...    -m
    ...    coverage    run
    ...    --parallel-mode
    ...    --branch
    ...    --source    JupyterLibrary
    ...    --context    atest-kernel-${OS}-${PY}-${LAB}-${ATTEMPT}
    ...    --concurrency    thread
    ...    --data-file    ${cov_path}${/}.coverage
    ...    @{rest}
    Set To Dictionary    ${spec_json}    argv=${argv}
    ${spec_text} =    Dumps    ${spec_json}    indent=${2}    sort_keys=${TRUE}
    Log    ${spec_text}
    Create File    ${spec_path}    ${spec_text}
