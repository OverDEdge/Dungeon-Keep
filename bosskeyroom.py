"""Boss Key Room class"""

from room import *

class BossKeyRoom(Room):
    def __init__(self, doors):
        super(BossKeyRoom, self).__init__(doors)
        self.chest = True
        self.chest_item = 'boss key'

    def enter(self, player):
        # Do special stuff for BossKeyRoom in case of search
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(BossKeyRoom, self).describe_room(self.came_from)
        # Print that there is a chest in the room
        print(dedent("""
        In the center of the room you notice a small ramp leading up
        to a large gold plated chest. As you move closer you notice that there seems
        to be a strange light eminating from the chest. You are mesmerized by the sight
        and wonder what riches might be hidden inside?!
        """))
        # If boss key is found then continue as standard room
        return super(BossKeyRoom, self).enter(player)
