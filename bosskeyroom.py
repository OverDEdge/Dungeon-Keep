"""Boss Key Room class"""

from room import *

class BossKeyRoom(Room):
    def __init__(self, doors):
        super(BossKeyRoom, self).__init__(doors)
        self.chest = True
        self.chest_item = 'boss key'

    def enter(self, player):
        # Do special stuff for BossKeyRoom in case of search

        # If boss key is found then continue as standard room
        return super(BossKeyRoom, self).enter(player)
