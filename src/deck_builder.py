from deck import Deck
import yaml
from card_type_provider import CardTypeProvider
from card_types.character import Character
from card import Card
import traceback
from deepmerge import always_merger
from copy import deepcopy

card_type_provider = CardTypeProvider()

def build_decks(library):
    decks = []
    for deck_name in library.get_decks():
        deck_info = library.get_deck_info(deck_name)
        deck = Deck(deck_name, deck_info, library)
        built_deck = build_deck(deck)
        decks.append(built_deck)

    return decks


def build_deck(deck: Deck):
    deck.cards = create_deck_cards(deck)
    return deck


def create_deck_cards(deck: Deck):
    cards = create_basic_cards(deck)
    cards.extend(create_collections(deck))
    return cards


def create_basic_cards(deck: Deck):
    return create_cards(deck.info.get('Cards', []), deck)


def create_collections(deck: Deck):
    cards = []
    for collection_name in deck.info.get('Collections', []):
        cards.extend(create_collection_cards(collection_name, deck))
    return cards


def create_collection_cards(collection_name, deck: Deck):
    collection = deck.library.get_collection(collection_name)
    cards = create_cards(collection.get('Cards', []), deck)
    for creature in collection.get('Equipment for', []):
        creature_info = resolve_card_info(creature, deck)
        if creature_info is not None:
            cards.extend(create_creature_equipment_collection(creature_info, deck))

    for creature in collection.get('Capabilities for', []):
        creature_info = resolve_card_info(creature, deck)
        if creature_info is not None:
            cards.extend(create_creature_capabilitiy_cards(creature_info, deck))

    for creature in collection.get('Skills for', []):
        creature_info = resolve_card_info(creature, deck)
        if creature_info is not None:
            cards.extend(create_creature_skill_cards(creature_info, deck))

    for creature in collection.get('Actions for', []):
        creature_info = resolve_card_info(creature, deck)
        if creature_info is not None:
            cards.extend(create_creature_action_cards(creature_info, deck))

    for creature in collection.get('Spells for', []):
        creature_info = resolve_card_info(creature, deck)
        if creature_info is not None:
            cards.extend(create_creature_spell_slot_cards(creature_info, deck))
            cards.extend(create_creature_spell_cards(creature_info, deck))

    return cards


def create_creature_equipment_collection(creature_info, deck: Deck):
    cards = []
    cards.extend(create_creature_weapon_cards(creature_info, deck))
    cards.extend(create_creature_armor_cards(creature_info, deck))
    cards.extend(create_creature_pack_cards(creature_info, deck))
    cards.extend(create_creature_item_cards(creature_info, deck))
    return cards


def create_creature_pack_cards(creature_info, deck: Deck):
    cards = []
    for pack_name in creature_info.get('Equipment', {}).get('Packs', []):
        pack_info = deck.library.get_pack_info(pack_name)
        cards.extend(create_cards(pack_info.get('Items', []), deck))
    return cards


def create_creature_item_cards(creature_info, deck: Deck):
    return create_cards(creature_info.get('Equipment', {}).get('Items', []), deck)

def create_creature_spell_slot_cards(creature_info, deck: Deck):
    cards = []
    for spell_slot_allocation_name in creature_info.get('Spell Slot Allocations', []):
        spell_slot_allocation_info = deck.library.get_spell_slot_allocation_info(spell_slot_allocation_name)
        print(spell_slot_allocation_info)
        cards.extend(create_cards(spell_slot_allocation_info.get('Spell Slots', []), deck))
    return cards

def create_creature_spell_cards(creature_info, deck: Deck):
    return create_cards_for_creature(creature_info.get('Spells', []), creature_info, deck)


def create_creature_armor_cards(creature_info, deck: Deck):
    return create_cards_for_creature(creature_info.get('Equipment', {}).get('Armor', []), creature_info, deck)


def create_creature_skill_cards(creature_info, deck: Deck):
    return create_cards_for_creature(get_skills_list(), creature_info, deck)


def create_creature_capabilitiy_cards(creature_info, deck: Deck):
    return create_cards_for_creature(creature_info.get('Capabilities', []), creature_info, deck)


def create_creature_action_cards(creature_info, deck: Deck):
    return create_cards_for_creature(creature_info.get('Actions', []), creature_info, deck)


def create_creature_weapon_cards(creature_info, deck: Deck):
    return create_cards_for_creature(creature_info.get('Equipment', {}).get('Weapons', []), creature_info, deck)


def create_copied_cards(card_name: str, quantity, deck):
    card_info = deck.library.get_card_info(card_name)
    if card_info is not None:
        return create_cards([card_name for _ in range(quantity)], deck)


def create_cards_for_creature(card_list, creature_info, deck):
    cards = create_cards(card_list, deck)
    for card in cards:
        card.creature_info = creature_info
    return cards


def create_cards(card_list, deck: Deck):
    cards = []
    for card_name in card_list:
        if type(card_name) is dict:
            card_name = next(iter(card_name))
        card = create_card(card_name, deck)
        if card is not None:
            cards.append(card)
    return cards


def create_card_for_creature(card_name: str, creature_info, deck):
    card = create_card(card_name, deck)
    card.creature_info = creature_info
    return card


def create_card(card_name: str, deck):
    try:
        card_info = resolve_card_info(card_name, deck)
        if card_info is not None:
            card_class = deck.card_type_provider.get_card_type(card_info.get('Type', ''))
            return card_class(card_name, card_info, deck.style)
        return None
    except Exception:
        traceback.print_exc()

def resolve_card_info(card_name: str, deck):
    card_info = deck.library.get_card_info(card_name)
    if card_info is not None:
        based_on = card_info.get('Based on', '')
        based_on_info = resolve_card_info(based_on, deck)
        if based_on_info is not None:
            return always_merger.merge(deepcopy(based_on_info), card_info)
    return deepcopy(card_info)

def get_skills_list():
    return [
        'Athletics',
        'Acrobatics',
        'Sleight of Hand',
        'Stealth',
        'Constitution',
        'Arcana',
        'History',
        'Investigation',
        'Passive Investigation',
        'Nature',
        'Religion',
        'Animal Handling',
        'Insight',
        'Medicine',
        'Perception',
        'Passive Perception',
        'Survival',
        'Deception',
        'Intimidation',
        'Performance',
        'Persuasion'
    ]