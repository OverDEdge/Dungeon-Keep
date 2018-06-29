"""Map Room class"""

from room import *

class MapRoom(Room):
    def __init__(self, doors):
        super(MapRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for MapRoom in case of search

        # If map is found then continue as standard room
        return super(MapRoom, self).enter(player)
