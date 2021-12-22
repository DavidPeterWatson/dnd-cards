import exceptions as exceptions
import version
import yaml
from deck_loader import load_deck
from deck_compiler import compile_deck
from deck_printer import print_deck
import click

@click.command()
@click.option('--deck', prompt='Deck file')
@click.option('--output', prompt='Output file',
              help='The person to greet.')
def build(deck, output):
    loaded_deck = load_deck(deck)
    compiled_deck = compile_deck(loaded_deck)
    print_deck(compiled_deck, output)


if __name__ == '__main__':
    build()