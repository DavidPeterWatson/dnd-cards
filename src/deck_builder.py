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

        for spell_name in deck.character_info.get('Prepared Spells', []):
            spell_info = deck.library.get_card_info(spell_name)
            if 'Type' not in spell_info:
                 print(f'no type specified for {spell_name}')
            else:
                spell_class = card_type_provider.get_card_type(spell_info['Type'])
                spell_card = spell_class(spell_name, spell_info, deck.style)
                deck.cards.append(spell_card)

        for weapon_name in deck.character_info.get('Equipment', {}).get('Weapons', []):
            weapon_info = deck.library.get_card_info(weapon_name)
            if 'Type' not in weapon_info:
                 print(f'no type specified for {weapon_name}')
            else:
                weapon_class = card_type_provider.get_card_type(weapon_info['Type'])
                weapon_card = weapon_class(weapon_name, weapon_info, deck.style)
                weapon_card.creature_info = deck.character_info
                deck.cards.append(weapon_card)

        for armor in deck.character_info.get('Equipment', {}).get('Armor', []):
            armor_info = deck.library.get_card_info(armor)
            if 'Type' not in armor_info:
                 print(f'no type specified for {armor}')
            else:
                armor_class = card_type_provider.get_card_type(armor_info['Type'])
                armor_card = armor_class(armor, armor_info, deck.style)
                armor_card.creature_info = deck.character_info
                deck.cards.append(armor_card)

        for capability in deck.character_info.get('Capabilities', []):
            capability_info = deck.library.get_card_info(capability)
            if 'Type' not in capability_info:
                 print(f'no type specified for {capability}')
            else:
                capability_class = card_type_provider.get_card_type(capability_info['Type'])
                capability_card = capability_class(capability, capability_info, deck.style)
                capability_card.creature_info = deck.character_info
                deck.cards.append(capability_card)

    # def is_in_deck(deck: Deck, card_info):
    #     if deck.info['Type'] == 'Character':
    #         character_info = deck.info['Cards'][deck.info['Character']]
    #         if card_info['Name'] in character_info.get('Prepared Spells', []):
    #              return True
    #         merged = list(set(card_info.get('Capabilities', [])) & set(character_info.get('Capabilities', [])))
    #         if len(merged) > 0:
    #             return True
    #     return False


    return deck