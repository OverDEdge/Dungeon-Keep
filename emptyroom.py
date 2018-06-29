"""Empty Room class"""

# EmptyRoom is basically the standard room.

from room import *

class EmptyRoom(Room):

    def __init__(self, doors):
        super(EmptyRoom, self).__init__(doors)

    def enter(self, player):
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(EmptyRoom, self).describe_room(self.came_from)

        return super(EmptyRoom, self).enter(player)
