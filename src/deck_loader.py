import yaml
import os
from deepmerge import always_merger

def load_deck(deck_filename):
    deck = open_deck(deck_filename)
    root_path = os.path.dirname(deck_filename)
    for filename in deck.get('Files', []):
        filepath = os.path.join(root_path, filename)
        loaded_deck = load_deck(filepath)
        deck = always_merger.merge(deck, loaded_deck)
    print(yaml.safe_dump(deck, sort_keys=False))
    deck['Root Folder'] = root_path
    return deck


def open_deck(deck_filename):
    with open(deck_filename) as file:
        deck = yaml.safe_load(file)
    return deck