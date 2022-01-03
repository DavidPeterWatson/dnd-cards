import exceptions as exceptions
import version
import yaml
from library_loader import load_library
from deck_builder import build_decks
from deck_printer import print_decks, Deck

import click

@click.command()
@click.option('--file', '-f', prompt='File')
def build(file):
    library = load_library(file)
    decks = build_decks(library)
    print_decks(decks)


if __name__ == '__main__':
    build()
