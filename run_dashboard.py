import click

from app.app import main


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
def cli(port, debug, workdir):
    """Run the Criticality Analysis Dashboard."""
    main(workdirs=workdir, port=port, debug=debug)


if __name__ == "__main__":
    cli()
