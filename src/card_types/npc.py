from card_types.creature import Creature

def get_class_name():
    return 'NPC'

def get_card_type():
    return 'NPC'

class NPC(Creature):

    def pre_draw(self):
        super().pre_draw()
        self.set_details()
        pass

        