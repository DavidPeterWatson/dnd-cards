from library_loader import load_library, load_library_info
from deck_builder import build_decks
from deck_renderer import render_decks
from version import __version__
import click
from database import Database, load_databases

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


@click.command('download', help='Download card data')
@click.option('--file', '-f', prompt='File')
def download(file):
    databases = load_databases(file)
    for database_info_name in databases:
        database = Database(database_info_name, databases[database_info_name])
        database.download()


@click.command('import', help='Import card data')
@click.option('--file', '-f', prompt='File')
def import_card_data(file):
    databases = load_databases(file)
    for database_info_name in databases:
        database = Database(database_info_name, databases[database_info_name])
        database.import_card_data()


cli.add_command(build)
cli.add_command(download)
cli.add_command(import_card_data)

if __name__ == '__main__':
    cli()

