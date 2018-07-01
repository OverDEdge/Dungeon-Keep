"""Map Room class"""

from room import *

class MapRoom(Room):
    def __init__(self, doors):
        super(MapRoom, self).__init__(doors)
        self.chest = True
        self.chest_open = True
        self.chest_item = 'map'

    def enter(self, player):
        # Do special stuff for MapRoom in case of search
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(MapRoom, self).describe_room(self.came_from)

        print(dedent("""
        As you survey the room you notice, in the corner, a small wooden chest. It looks
        worn with age and the lid is gone.
        """))

        # If map is found then continue as standard room
        return super(MapRoom, self).enter(player)
