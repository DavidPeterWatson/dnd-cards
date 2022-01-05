from library_loader import load_library
from deck_builder import build_decks
from deck_renderer import render_decks
from version import __version__

import click

@click.command()
@click.option('--file', '-f', prompt='File')
def build(file):
    library = load_library(file)
    decks = build_decks(library)
    render_decks(decks)

# @click.command('--version', '-v', prompt='File')
# def version(file):
#     print(__version__)

if __name__ == '__main__':
    build()
