from deck import Deck
import yaml
from card_type_provider import CardTypeProvider
from card_types.character import Character

def build_decks(library):
    decks = []
    for deck_name in library.get_decks():
        deck_info = library.get_deck_info(deck_name)
        deck = Deck(deck_name, deck_info, library)
        built_deck = build_deck(deck)
        decks.append(built_deck)

    return decks


def build_deck(deck: Deck):
    card_type_provider = CardTypeProvider()

    if deck.type == 'Character':
        character_card = Character(deck.character_name, deck.character_info, deck.style)
        deck.cards.append(character_card)

        for pack_name in deck.character_info['Equipment'].get('Packs', []):
            pack_info = deck.library.get_pack_info(pack_name)
            for item in pack_info.get('Items', []):
                item_info = deck.library.get_card_info(item)
                if 'Type' not in item_info:
                    print(f'no type specified for {item}')
                else:
                    card_class = card_type_provider.get_card_type(item_info['Type'])
                    item_card = card_class(item, item_info, deck.style)
                    deck.cards.append(item_card)

        for coinage in deck.character_info['Equipment'].get('Coinage', []):
            coin_type = coinage['Coin Type']
            coin_info = deck.library.get_card_info(coin_type)
            if 'Type' not in coin_info:
                 print(f'no type specified for {item}')
            else:
                coin_class = card_type_provider.get_card_type(coin_info['Type'])
                coin_card = coin_class(coin_type, coin_info, deck.style, coinage['Quantity'])
                deck.cards.append(coin_card)

    return deck