from card_types.creature import Creature
import traceback
import yaml

def get_class_name():
    return 'Character'

class Character(Creature):

    def pre_draw(self):
        super().pre_draw()
        self.add_carrying_capacity()
        self.set_categories()
        pass


    # def build_deck(self):
    #     for pack in self.info['Equipment'].get('Packs', []):
    #         print(pack)
    #         pack_info = self.deck.packs.get(pack, {})
    #         print(yaml.safe_dump(pack_info))
    #         for gear in pack_info.get('Gear', []):
    #             if gear in self.deck.cards:
    #                 self.info['Equipment']['Gear'].append(gear)

    #     for coinage in self.info['Equipment'].get('Coinage', []):
    #         coin_type = coinage['Coin Type']
    #         quantity = coinage['Quantity']
    #         coinage_name = f'{quantity} of {coin_type}'
    #         coinage_info = self.deck.cards.get(coinage['Coin Type'], {})
    #         self.deck.cards[coinage_name] = coinage_info
    #         self.info['Equipment']['Gear'].append(coinage_name)


    def set_categories(self):
        self.info['Category'] = self.info.get('Subrace') + ' ' + self.info.get('Race')
        self.info['Subcategory'] = self.info.get('Class')


    def is_in_deck(deck, card_info):
        return True
