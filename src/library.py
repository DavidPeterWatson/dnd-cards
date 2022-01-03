class Library():
    def __init__(self, library_info, root_path):
        self.info = library_info
        self.root_path = root_path

    def get_card_info(self, card_name):
        return self.info.get('Cards', {}).get(card_name, {})


    def get_pack_info(self, pack_name):
        return self.info.get('Packs', {}).get(pack_name, {})


    def get_style(self, style_name):
        return self.info.get('Styles', {}).get(style_name, {})


    def get_deck_info(self, deck_name):
        return self.info.get('Decks', {}).get(deck_name, {})


    def get_decks(self):
        return self.info.get('Decks', {})
