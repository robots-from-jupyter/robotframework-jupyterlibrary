""" Documentation configuration and workflow for JupyterLibrary
"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from configparser import ConfigParser

# you have to have run `python -m pip install -e`
import JupyterLibrary
from JupyterLibrary.core import CLIENTS, COMMON

# not really in use yet...
os.environ["IN_SPHINX"] = "1"

_parser = ConfigParser()
_parser.read(Path(__file__).parent.parent / "setup.cfg")

CONF = {k: _parser[k] for k in _parser.sections()}
YEAR = datetime.now().year
KEYWORDS = "*** Keywords ***"
VARIABLES = "*** Variables ***"


def setup(app):
    """Runs before the "normal business" of sphinx. Don't go too crazy here."""
    here = Path(__file__).parent

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "robot.libdoc",
            "JupyterLibrary",
            str(here / "_static" / "JupyterLibrary.html"),
        ]
    )

    for client_dir in CLIENTS:
        client = Path(client_dir)
        print(client.name)
        with TemporaryDirectory() as td:
            tdp = Path(td)
            agg = "\n".join(
                [
                    "*** Settings ***",
                    f"Documentation    Keywords for {client.name}",
                    "",
                ]
            )
            for sub in sorted(client.rglob("*.resource")):
                sub_text = sub.read_text()
                has_vars = VARIABLES in sub_text
                has_kw = KEYWORDS in sub_text
                print(f"... collecting {sub.relative_to(client)}")
                print(f"    ... keywords?  {has_kw}")
                print(f"    ... variables? {has_vars}")

                split_on = VARIABLES if has_vars else KEYWORDS
                agg += "\n".join([split_on, sub_text.split(split_on)[1], ""])
            out_file = Path(tdp / f"{client.name}.resource")
            out_file.write_text(agg)
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "robot.libdoc",
                    str(out_file),
                    str(here / "_static" / f"{client.name}.html"),
                ]
            )

    for common_file in COMMON:
        common = Path(common_file)
        common_name = common.name.lower().replace(".resource", "")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "robot.libdoc",
                common,
                str(here / "_static" / f"{common_name}.html"),
            ]
        )

    app.add_css_file("css/custom.css")


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = CONF["metadata"]["name"]
copyright = f"""{YEAR}, {CONF["metadata"]["author"]}"""
author = CONF["metadata"]["author"]

# The short X.Y version
version = ".".join(JupyterLibrary.__version__.split(".")[:2])
# The full version, including alpha/beta/rc tags
release = JupyterLibrary.__version__

# for now
language = "en"

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "myst_nb",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [".ipynb_checkpoints", "**/.ipynb_checkpoints"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "material"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "page_sidebar_items": [],
    "navbar_center": ["navbar-nav", "navbar-icon-links"],
    "navbar_end": [],
    "github_url": CONF["metadata"]["url"],
}

html_sidebars = {
    "**": [
        "search-field",
        "page-toc",
        "edit-this-page",
        "sidebar-nav-bs",
        "sidebar-ethical-ads",
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

jupyter_execute_notebooks = "force"

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = f"""{CONF["metadata"]["name"]}-doc"""


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"""{CONF["metadata"]["name"]}.tex""",
        f"""{CONF["metadata"]["name"]} Documentation""",
        CONF["metadata"]["author"],
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        CONF["metadata"]["name"],
        f"""{CONF["metadata"]["name"]} Documentation""",
        [author],
        1,
    )
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "jupyterlibrary",
        f"""{CONF["metadata"]["name"]} Documentation""",
        author,
        CONF["metadata"]["name"],
        CONF["metadata"]["description"],
        "Miscellaneous",
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
