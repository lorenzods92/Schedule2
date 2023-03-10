# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Schedule2'
copyright = '2023, LDS'
author = 'LDS'
release = '0.0.9'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

#"myst_parser" to create html from .md legge da markdown [3rd party]
#"sphinx.ext.duration" to compute duration
#"sphinx.ext.autosectionlabel" permette hyperlinks con altre sezioni {ref}
#"nbsphinx" per jupyter [3rd party]
# "sphinx.ext.autodoc" genero automaticamente docum. da python
extensions = ["myst_parser", 
             "sphinx.ext.duration",
             "sphinx.ext.autosectionlabel",
             "sphinx.ext.autodoc",
             ]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
