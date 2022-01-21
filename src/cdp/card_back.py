from cdp.position import Position
from cdp.card import Card

class CardBack():
    def __init__(self, card: Card, front_position: Position):
        self.card = card
        self.front_position = front_position
    
    def draw_back(self):
        self.card.draw_back(self.front_position.get_back_position())