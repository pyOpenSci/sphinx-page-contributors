"""Currently using mamba envt: contributors for pygithub

This is the mkdocs plugin
https://github.com/byrnereese/mkdocs-git-committers-plugin/blob/master/mkdocs_git_committers_plugin/plugin.py

# Install extension
pip install -e .
# Build docs
sphinx-build -b html . _build/html

https://www.sphinx-doc.org/en/master/development/tutorials/helloworld.html

For this to work, setup your GITHUB token in your zsh, bashprofile envt

Right now this is slow as it will process all commits for each file. 
Instead we probably want to create some sort of cache that has a history of
what has been processed. so it them only processes the most recent commits 
and files. 

we also want to allow it to ignore some files (which could be a sphinx conf.py 
setting)
"""

import os

from github import Github

print("Loading contributors extension.")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "pyopensci/python-package-guide"

github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)


def fetch_unique_committers(app, docname, source):
    """
    Fetch the unique committers for a given document and store the data in the
    Sphinx environment.

    This function is called by Sphinx for each document due to the connection
    established
    in the setup function to the 'source-read' event. It fetches the committers
      for the document
    based on its GitHub commit history.

    Parameters
    ----------
    app : Sphinx application object
        The Sphinx application context which provides access to Sphinx's
        configurations and methods.
    docname : str
        The name of the document being processed, which corresponds to the
        file name without the extension.
    source : list
        The list containing the source content of the document. The list has a
        single element, which is a string.
    """

    # if docname in app.config.ignore_files:
    #     return

    file_path = f"{docname}.md"
    print("Fetching committers for:", file_path)
    unique_committers = get_unique_committers(
        GITHUB_TOKEN, REPO_NAME, file_path
    )
    print("Committers are", unique_committers)
    # Store committers in the environment to be used later in the build
    if not hasattr(app.env, "committers_data"):
        app.env.committers_data = {}

    app.env.committers_data[docname] = unique_committers

    # Append to markdown file instead as a test???
    committer_list = "\n".join(
        [
            f"- {committer['name']} ([@{committer['login']}]({committer['profile_url']}))"
            for committer in unique_committers
        ]
    )
    markdown_contributors = f"\n\n## Contributors\n{committer_list}\n"

    # Append this markdown to the original document source
    source[0] += markdown_contributors


def add_committers_to_context(app, pagename, templatename, context, doctree):
    """
    Add committer data to the HTML page context if available.

    This function is connected to the 'html-page-context' event in Sphinx.
    It's called before rendering
    the HTML page, allowing the injection of additional data into the page
    context.

    Parameters
    ----------
    app : Sphinx application object
        The Sphinx application context.
    pagename : str
        The name of the page being rendered.
    templatename : str
        The name of the template being used.
    context : dict
        The context dictionary that the template will use. You can add
        additional data to this dictionary.
    doctree : document tree node
        The doctree of the page, which can be used to extract additional
        metadata or content if needed.
    """

    if (
        hasattr(app.env, "committers_data")
        and pagename in app.env.committers_data
    ):
        context["committers"] = app.env.committers_data[pagename]


def get_unique_committers(github_token, repo_name, file_path):
    commits = repo.get_commits(path=file_path)
    unique_committers = set()

    for commit in commits:
        if commit.author:
            unique_committers.add(commit.author.login)

    committers_info = []
    for login in unique_committers:
        user = github.get_user(login)
        committers_info.append(
            {
                "login": user.login,
                "name": user.name,
                "avatar_url": user.avatar_url,
                "profile_url": f"https://github.com/{login}",
            }
        )

    return committers_info


# def list_markdown_files(repo):
#     """
#     List all Markdown files in the repository.
#     NOTE: this will also return readme and other files that we may not want
#     to consider.
#     """
#     markdown_files = []
#     contents = repo.get_contents("")  # Start at the root directory
#     while contents:
#         file_content = contents.pop(0)
#         if file_content.type == "dir":
#             contents.extend(
#                 repo.get_contents(file_content.path)
#             )  # Add directory contents to list
#         elif file_content.path.endswith(".md"):
#             markdown_files.append(file_content.path)
#     return markdown_files


# def get_unique_committers(github_token, repo_name, file_path):
#     # Here this will be getting a repo online. but generally this
#     # will be run as the docs are built in CI or locally. so
#     # this approach doesnt make sense to me.

#     commits = repo.get_commits(path=file_path)
#     unique_committers = set()

#     for commit in commits:
#         if commit.author:
#             unique_committers.add(commit.author.login)

#     committers_info = []
#     for login in unique_committers:
#         user = github.get_user(login)
#         committers_info.append(
#             {
#                 "login": user.login,
#                 "name": user.name,
#                 "avatar_url": user.avatar_url,
#                 "profile_url": f"https://github.com/{login}",
#             }
#         )

#     return committers_info


# md_files = list_markdown_files(repo)

# # Process each markdown file and get contributors
# people = {}
# for gh_file in md_files:
#     print("Processing: ", gh_file)
#     people[gh_file] = get_unique_committers(GITHUB_TOKEN, REPO_NAME, gh_file)
