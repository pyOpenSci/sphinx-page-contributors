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
from sphinx.application import Sphinx

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "pyopensci/python-package-guide"

github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)


def setup(app: Sphinx):
    app.connect("source-read", get_unique_committers)


def list_markdown_files(repo):
    """
    List all Markdown files in the repository.
    NOTE: this will also return readme and other files that we may not want
    to consider.
    """
    markdown_files = []
    contents = repo.get_contents("")  # Start at the root directory
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(
                repo.get_contents(file_content.path)
            )  # Add directory contents to list
        elif file_content.path.endswith(".md"):
            markdown_files.append(file_content.path)
    return markdown_files


def get_unique_committers(github_token, repo_name, file_path):
    # Here this will be getting a repo online. but generally this
    # will be run as the docs are built in CI or locally. so
    # this approach doesnt make sense to me.

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


md_files = list_markdown_files(repo)

people = {}
for gh_file in md_files:
    print("Processing: ", gh_file)
    people[gh_file] = get_unique_committers(GITHUB_TOKEN, REPO_NAME, gh_file)
