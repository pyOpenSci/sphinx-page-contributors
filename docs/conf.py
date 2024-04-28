# Sphinx docs config

project = "sphinx-contribs"
copyright = "2024, pyOpenSci Community"
author = "pyOpenSci Community"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx-contribs"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata-sphinx-theme"
html_static_path = ["_static"]
