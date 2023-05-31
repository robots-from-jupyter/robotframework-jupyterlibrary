*** Settings ***
Documentation       Common behaviors for CodeMirror instances


*** Variables ***
${CM VERSION}           ${5}
# the accessor from the DOM element for a JS instance
${CM JS INSTANCE}       .CodeMirror
# a CodeMirror DOM element
${CSS CM EDITOR}        .CodeMirror


*** Keywords ***
Call CodeMirror Method
    [Documentation]    Construct and a method call against in the CodeMirror attached to the element
    ...    that matches a ``css`` selector with the given ``js`` code.
    ...    The CodeMirror editor instance will be available as `cm`.
    [Arguments]    ${css}    ${js}
    ${result} =    Execute JavaScript
    ...    (() => {
    ...    const cm = document.querySelector(`${css}`)${CM JS INSTANCE};
    ...    return cm.${js};
    ...    }).call(this);
    [Return]    ${result}

Execute CodeMirror Command
    [Documentation]    Run a CodeMirror [https://codemirror.net/doc/manual.html#commands:command]
    ...    ``cmd`` for the editor attached to element that matches a ``css`` selector.
    ...    Only works for CodeMirror 5.
    [Arguments]    ${css}    ${cmd}
    Call CodeMirror Method    ${css}    execCommand("${cmd}")

Set CodeMirror Value
    [Documentation]    Set the value in the CodeMirror attached to the element
    ...    that matches a ``css`` selector to be the given ``text``.
    [Arguments]    ${css}    @{code}
    Select All CodeMirror Text    ${css}
    ${res} =    Replace CodeMirror Selection    ${css}    @{code}
    [Return]    ${res}

Select All CodeMirror Text
    [Documentation]    Select all of the text in the CodeMirror attached to the element
    ...    matched by a ``css`` selector.
    [Arguments]    ${css}
    ${res} =    Run Keyword    Select All CodeMirror ${CM VERSION} Text    ${css}
    [Return]    ${res}

Select All CodeMirror 5 Text
    [Documentation]    Select all of the text in the CodeMirror 5 attached to the element
    ...    matched by a ``css`` selector.
    [Arguments]    ${css}
    ${res} =    Execute CodeMirror Command    ${css}    selectAll
    [Return]    ${res}

Select All CodeMirror 6 Text
    [Documentation]    Select all of the text in the CodeMirror 6 attached to the element
    ...    matched by a ``css`` selector.
    [Arguments]    ${css}
    ${res} =    Call CodeMirror Method    ${css}
    ...    view.dispatch({selection: {anchor: 0, head: cm.view.state.doc.length}})
    [Return]    ${res}

Replace CodeMirror Selection
    [Documentation]    Replace all of the text in the CodeMirror attached to the element
    ...    that matches a ``css`` selector with the given ``text``.
    [Arguments]    ${css}    @{code}
    ${res} =    Run Keyword    Replace CodeMirror ${CM VERSION} Selection    ${css}    @{code}
    [Return]    ${res}

Replace CodeMirror 5 Selection
    [Documentation]    Replace all of the text in the CodeMirror 5 attached to the element
    ...    that matches a ``css`` selector with the given ``text``.
    [Arguments]    ${css}    @{code}
    ${value} =    Evaluate    """\n""".join(${code})
    ${res} =    Call CodeMirror Method    ${css}    replaceSelection(`${value}`)
    [Return]    ${res}

Replace CodeMirror 6 Selection
    [Documentation]    Replace all of the text in the CodeMirror 6 attached to the element
    ...    that matches a ``css`` selector with the given ``text``.
    [Arguments]    ${css}    @{code}
    ${value} =    Evaluate    """\n""".join(${code})
    ${res} =    Call CodeMirror Method    ${css}
    ...    view.dispatch(cm.view.state.replaceSelection(`${value}`))
    [Return]    ${res}
