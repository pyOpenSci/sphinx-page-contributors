# Sphinx docs config

import sphinx_contribs

project = "Sphinx Contributor Extension"
copyright = "2024, pyOpenSci Community"
author = "pyOpenSci Community"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_contribs",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# Settings for sphinx-contribs ext
repo_name = "pyopensci/python-package-guide"

# html_theme_options = {navigation_with_keys: False}
