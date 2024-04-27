"""Currently using mamba envt: contributors for pygithub"""

from github import Github

# Replace these with actual values
GITHUB_TOKEN = "your_github_token_here"
#GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "owner/repo"
FILE_PATH = "path/to/file"


def get_unique_committers(github_token, repo_name, file_path):
    github = Github(github_token)
    repo = github.get_repo(repo_name)
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


committers = get_unique_committers(GITHUB_TOKEN, REPO_NAME, FILE_PATH)
for committer in committers:
    print(committer)
