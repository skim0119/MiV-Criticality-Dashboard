import subprocess

import requests


def get_local_commit_hash():
    """Get the current git commit hash of the local repository."""
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_remote_commit_hash():
    """Get the latest commit hash from the remote repository."""
    try:
        # Get the remote URL
        remote_url = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        # Convert SSH URL to HTTPS if needed
        if remote_url.startswith("git@"):
            remote_url = remote_url.replace("git@github.com:", "https://github.com/")
            remote_url = remote_url.replace(".git", "")

        # Get the repository name from the URL
        repo_name = remote_url.split("/")[-2] + "/" + remote_url.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        # Get the latest commit hash from GitHub API
        api_url = f"https://api.github.com/repos/{repo_name}/commits/main"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()["sha"]
    except Exception:
        return None
