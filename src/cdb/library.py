class Library():
    def __init__(self, library_info, root_path):
        self.info = library_info
        self.root_path = root_path

    def get_card_info(self, card_name):
        return self.info.get('Cards', {}).get(card_name, None)


    def get_pack_info(self, pack_name):
        return self.info.get('Packs', {}).get(pack_name, {})

    def get_spell_slot_allocation_info(self, spell_slot_allocation_name):
        return self.info.get('Spell Slot Allocations', {}).get(spell_slot_allocation_name, {})

    def get_style(self, style_name):
        return self.info.get('Styles', {}).get(style_name, {})


    def get_deck_info(self, deck_name):
        return self.get_decks().get(deck_name, {})


    def get_decks(self):
        return self.info.get('Decks', {})


    def get_collections(self):
        return self.info.get('Collections', {})

    def get_collection(self, collection_name):
        return self.info.get('Collections', {}).get(collection_name, {})
