"""
This file defines the Player class.
Each Player object has:
Health, Attack, Defence and Agility stats which help in monster encounters
"""

# The stats are defined in the dictionary STATS where:
# - PLAYER_STATS[0] = Health
# - PLAYER_STATS[1] = Attack
# - PLAYER_STATS[2] = Defence
# - PLAYER_STATS[3] = Agility
PLAYER_STATS = {
"Paladin": [100, 20, 15, 5],
"Ranger": [70, 15, 10, 15],
"Thief": [60, 10, 10, 20],
"Sorcerer": [75, 15, 10, 10]
}

# Player is Super class which have the common elements of each character type.
# Player shall have elements:
# health, attack, defence and agility
# position (tuple)
# items (list)
# type (string, default "Paladin")
# locations (list of positions where player has been)
# prev_pos (previous position needs to be know if Player flees)
# name (string to print, default "Link")
class Player:

    def __init__(self, x, y, type = "Paladin", name = "Link"):
        self.health = PLAYER_STATS[type][0]
        self.attack = PLAYER_STATS[type][1]
        self.defence = PLAYER_STATS[type][2]
        self.agility = PLAYER_STATS[type][3]
        self.position = (x, y)
        self.items = []
        self.type = type
        self.locations = [(x, y)]
        self.prev_pos = (x, y)
        self.name = name

    # When player position is updated the position and locations variables
    # shall be updated
    def update_pos(self, x, y):
        self.prev_pos = self.position
        self.position = (x, y)
        # If new position not in locations then append to locations list
        if self.position not in self.locations:
            self.locations.append(self.position)

class Ranger(Player):

    def __init__(self, x, y, name):
        super(Ranger, self).__init__(x, y, "Ranger", name)

class Thief(Player):

    def __init__(self, x, y, name):
        super(Thief, self).__init__(x, y, "Thief", name)

class Sorcerer(Player):

    def __init__(self, x, y, name):
        super(Sorcerer, self).__init__(x, y, "Sorcerer", name)

class Paladin(Player):

    def __init__(self, x, y, name):
        super(Paladin, self).__init__(x, y, "Paladin", name)

#p = Paladin(1,1, "Rimmer")
#print(str(p.health) + " " + p.name)
