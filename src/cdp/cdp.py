from cdp.library_loader import load_library, load_library_info
from cdp.deck_builder import build_decks
from cdp.deck_printer import render_decks
from cdp.version import __version__
import click
from cdp.database import download_databases, import_databases

CONFIG_FILE_NAME = 'cdb_config.yaml'


@click.group()
@click.version_option(__version__)
def cli():
    pass


@click.command('print', help='Print a deck')
@click.option('--file', '-f', prompt='Deck file name')
def print(file):
    library_info = load_library_info(CONFIG_FILE_NAME)
    library = load_library(file, library_info)
    decks = build_decks(library)
    render_decks(decks)


@click.command('download', help='Download card data')
@click.option('--file', '-f', prompt='File')
def download(file):
    download_databases(file)


@click.command('import', help='Import card data')
@click.option('--file', '-f', prompt='File')
def import_card_data(file):
    import_databases(file)


cli.add_command(print)
cli.add_command(download)
cli.add_command(import_card_data)

if __name__ == '__main__':
    cli()

