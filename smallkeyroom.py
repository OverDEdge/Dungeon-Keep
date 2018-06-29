"""Small Key Room class"""

from room import *

class SmallKeyRoom(Room):
    def __init__(self, doors):
        super(SmallKeyRoom, self).__init__(doors)
        self.corpse = True
        self.corpse_item = 'small key'

    def enter(self, player):
        # Do special stuff for SmallKeyRoom in case of search

        # If small key is found then continue as standard room
        return super(SmallKeyRoom, self).enter(player)
