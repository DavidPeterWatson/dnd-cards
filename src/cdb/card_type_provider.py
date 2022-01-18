import os
import logging
import importlib
import traceback
import card_types.basic
import card_types.action
import card_types.armor
import card_types.character
import card_types.condition
import card_types.creature
import card_types.item
import card_types.magical_item
import card_types.narrative
import card_types.passive_skill
import card_types.prop
import card_types.skill
import card_types.spell_slot
import card_types.spell
import card_types.weapon

logging.getLogger().setLevel(logging.INFO)

CARD_TYPES_FOLDER = 'card_types'

class CardTypeProvider:

    def __init__(self):
        self.card_types = self.load_card_types()
        self.card_types['Action'] = card_types.action.Action
        self.card_types['Basic'] = card_types.basic.Basic
        self.card_types['Armor'] = card_types.armor.Armor
        self.card_types['Character'] = card_types.character.Character
        self.card_types['Condition'] = card_types.condition.Condition
        self.card_types['Creature'] = card_types.creature.Creature
        self.card_types['Item'] = card_types.item.Item
        self.card_types['MagicalItem'] = card_types.magical_item.MagicalItem
        self.card_types['Narrative'] = card_types.narrative.Narrative
        self.card_types['Skill'] = card_types.passive_skill.Skill
        self.card_types['Prop'] = card_types.prop.Prop
        self.card_types['Skill'] = card_types.skill.Skill
        self.card_types['SpellSlot'] = card_types.spell_slot.SpellSlot
        self.card_types['Spell'] = card_types.spell.Spell
        self.card_types['Weapon'] = card_types.weapon.Weapon

    def get_card_type(self, card_type: str):
        return self.card_types.get(card_type, card_types.basic.Basic)


    def load_card_types(self):
        card_types = {}
        # for filename in filter(lambda x: x.endswith('.py') and x != '__init__.py', os.listdir(CARD_TYPES_FOLDER)):
        #     try:
        #         card_type, card_class = self.load_card_type('{}.{}'.format(CARD_TYPES_FOLDER, filename[:-3]))
        #         card_types[card_type] = card_class
        #     except Exception as e:
        #         logging.error(e, exc_info=True)
        return card_types


    def load_card_type(self, filename):
        module = importlib.import_module(filename)
        class_name = module.get_class_name()
        card_type = module.get_card_type()
        return card_type, getattr(module, class_name)
