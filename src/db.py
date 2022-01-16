from library_loader import load_library, load_library_info
from deck_builder import build_decks
from deck_renderer import render_decks
from version import __version__
import click

CONFIG_FILE_NAME = 'db_config.yaml'


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command('build', help='Build a deck')
@click.option('--file', '-f', prompt='File')
def build(file):
    library_info = load_library_info(CONFIG_FILE_NAME)
    library = load_library(file, library_info)
    decks = build_decks(library)
    render_decks(decks)


@click.command('update', help='Update card data')
@click.option('--file', '-f', prompt='File')
def update(file):
    pass


cli.add_command(build)
cli.add_command(update)

if __name__ == '__main__':
    cli()

