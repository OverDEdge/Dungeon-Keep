"""PLayer Room class"""

from room import *

class PlayerRoom(Room):
    def __init__(self, doors):
        super(PlayerRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for PlayerRoom
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(PlayerRoom, self).describe_room(self.came_from)
        # Then continue as standard room
        return super(PlayerRoom, self).enter(player)
