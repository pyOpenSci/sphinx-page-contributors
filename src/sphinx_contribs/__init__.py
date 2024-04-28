from sphinx.application import Sphinx

from .contribs import fetch_unique_committers


def setup(app: Sphinx):
    """The setup function for Sphinx. This connects the sphinx processing to
    the functions in this module.

    Parameters
    ----------
    app : Sphinx
        _description_
    """
    app.connect("source-read", fetch_unique_committers)
    # app.connect("html-page-context", add_committers_to_context)
    # app.add_config_value("ignore_files", [], "env")
