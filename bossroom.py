"""Boss Room class"""

from room import *

class BossRoom(Room):

    def __init__(self, doors):
        super(BossRoom, self).__init__(doors)
        self.boss_door = True

    def enter(self, player):
        # Do special stuff for BossRoom
        pass
        # If boss is passed defeated game ends
