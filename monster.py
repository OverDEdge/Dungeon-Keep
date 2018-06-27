"""
This file defines the Monster class.
Each Monster object has:
Health, Attack, Defence and Agility stats which help in monster encounters
"""

# The stats are defined in the dictionary STATS where:
# - MONSTER_STATS[0] = Health
# - MONSTER_STATS[1] = Attack
# - MONSTER_STATS[2] = Defence

MONSTER_STATS = {
"Skeleton": [10, 10, 5],
"Goblin": [5, 5, 10],
"Dark Elf": [5, 5, 5],
}

BOSS_STATS = {
"Dragon": [50, 20, 10]
}

# Monster is Super class which have the common elements of each character type.
# Monster shall have elements:
# health, attack and defence
# type (string, default "Skeleton")

class Monster:

    def __init__(self, type = "Skeleton"):
        self.health = MONSTER_STATS[type][0]
        self.attack = MONSTER_STATS[type][1]
        self.defence = MONSTER_STATS[type][2]
        self.type = type

class Skeleton(Monster):

    def __init__(self):
        super(Skeleton, self).__init__("Skeleton")

class Goblin(Monster):

    def __init__(self):
        super(Goblin, self).__init__("Goblin")

class DarkElf(Monster):

    def __init__(self):
        super(DarkElf, self).__init__("Dark Elf")

class Dragon(Monster):

    def __init__(self, type = "Dragon"):
        self.health = BOSS_STATS[type][0]
        self.attack = BOSS_STATS[type][1]
        self.defence = BOSS_STATS[type][2]
        self.type = type
