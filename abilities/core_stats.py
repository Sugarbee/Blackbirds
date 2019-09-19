"""
Abilities representing a character's physical characteristics.
"""
from abilities.ability import Ability as BaseAbility
from abilities.ability import AbilityTree as BaseAbilityTree

# ------------------------------------------------------------------------------

class Might(BaseAbilityTree):
    def at_ability_creation(self):
        self.description = "An indication of the character's overall physical prowess and athleticism."

    def at_ability_tree_creation(self):
        self.add_ability(Strength())

class Strength(BaseAbility):
    def at_ability_creation(self):
        self.description = "The character's physical strength."

# ------------------------------------------------------------------------------

class Dexterity(BaseAbilityTree):
    "The character's agility, speed, and reflexes."
    def at_ability_tree_creation(self):
        self.add_ability(Agility())

class Agility(BaseAbility):
    def at_ability_creation(self):
        self.description = "Represents the character's ability to leap, roll, or otherwise maneuver."

# ------------------------------------------------------------------------------

class Acuity(BaseAbilityTree):
    "The character's perception - ability to see, hear, or sense things."
    def at_ability_tree_creation(self):
        self.add_ability(Vision())

class Vision(BaseAbility):
    def at_ability_creation(self):
        self.description = "How far or how sharply the character can see. Confers a bonus to spotting hidden players and objects."