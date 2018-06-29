"""Exit Room class"""

from room import *

class ExitRoom(Room):
    def __init__(self, doors):
        super(ExitRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for ExitRoom -> End Game
        # If not quit continue as normal

        return super(ExitRoom, self).enter(player)
