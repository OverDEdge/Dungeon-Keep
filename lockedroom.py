"""Locked Room class"""

from room import *

class LockedRoom(Room):
    def __init__(self, doors):
        super(LockedRoom, self).__init__(doors)
        self.door = True

    def enter(self, player):
        # Do special stuff for LockedRoom in case of search

        # If unlocked room then continue as standard room
        return super(LockedRoom, self).enter(player)
