import click

from . import __version__
from .server import run_forever
from .settings import load_settings


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option('--env-path',
              type=click.Path(exists=True, readable=True, resolve_path=True),
              help='Dot env file or directory path.')
def run(env_path: str):
    """
    Runs the application.
    """
    config = load_settings(env_path)
    run_forever(config)
