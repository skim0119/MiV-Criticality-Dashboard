import subprocess
import sys

import click
import requests

from app.app import main


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


def check_version():
    """Check if the local version matches the remote version."""
    local_hash = get_local_commit_hash()
    remote_hash = get_remote_commit_hash()

    return local_hash, remote_hash


@click.command()
@click.option("--port", default=5000, help="Port to run the server on.")
@click.option("--debug", is_flag=True, help="Debug mode flag")
@click.option(
    "--workdir",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    multiple=True,
    help="Working cache directory.",
)
@click.option(
    "--skip-version-check",
    is_flag=True,
    help="Skip checking if the local version matches the remote version.",
)
def cli(port, debug, workdir, skip_version_check):
    """Run the Criticality Analysis Dashboard."""
    if not skip_version_check:
        local_hash, remote_hash = check_version()
        if local_hash is None or remote_hash is None:
            click.echo(click.style("Warning: Unable to check version. Continuing with default behavior.", fg="yellow"))
        elif local_hash != remote_hash:
            click.echo(
                click.style(
                    "\nVersion Check Warning:\n"
                    f"Local version:  {local_hash}\n"
                    f"Remote version: {remote_hash}\n\n"
                    "Your local version appears to be outdated. "
                    "Consider pulling the latest changes from the repository.\n"
                    "You can skip this check using --skip-version-check flag.\n",
                    fg="yellow",
                )
            )
            if not click.confirm("Do you want to continue anyway? [y/N]"):
                sys.exit(1)

    main(workdirs=workdir, port=port, debug=debug)


if __name__ == "__main__":
    cli()
