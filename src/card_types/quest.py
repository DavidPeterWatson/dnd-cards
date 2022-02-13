from cdp.card import Card
import traceback

def get_class_name():
    return 'Quest'

def get_card_type():
    return 'Quest'

class Quest(Card):

    def draw_specifications(self, position):
        try:
            reward = self.info.get('Reward', 'reward')
            self.draw_specification('Reward', reward, position)

        except Exception:
            traceback.print_exc()

    def has_specifications(self):
        return True
