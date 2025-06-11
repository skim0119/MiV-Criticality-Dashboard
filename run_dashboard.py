import sys

import click

from app.app import main
from app.git_utils import get_local_commit_hash, get_remote_commit_hash


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
        local_hash = get_local_commit_hash()
        remote_hash = get_remote_commit_hash()
        if local_hash is None or remote_hash is None:
            click.echo(
                click.style(
                    "Warning: Unable to check version. Continuing with default behavior.",
                    fg="yellow",
                )
            )
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
            if not click.confirm("Do you want to continue anyway?"):
                click.echo(click.style("Exiting...", fg="red"))
                sys.exit(1)
            else:
                click.echo(click.style("Continuing...", fg="green"))

    main(workdirs=workdir, port=port, debug=debug)


if __name__ == "__main__":
    cli()
