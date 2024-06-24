import os
import sys
sys.path.insert(0, os.path.abspath("../"))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project: str = 'SS7 Op.Python実行マニュアル'
copyright: str = '2024, KG17492'
author: str = 'KG17492'
release: str = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    "myst_parser",
    "sphinx.ext.autodoc",
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

myst_enable_extensions: list[str] = [
    "dollarmath",
    "html_image",
]

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = ['_build', 'Thumbs.db', '.DS_Store']

language: str = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme: str = 'sphinx_rtd_theme'
html_static_path: list[str] = ['_static']
html_style: str = "css/mytheme.css"
html_favicon: str = "img/favicon.ico"
source_suffix: dict[str, str] = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
