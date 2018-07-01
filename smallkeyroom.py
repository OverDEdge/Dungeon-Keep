"""Small Key Room class"""

from room import *

class SmallKeyRoom(Room):
    def __init__(self, doors):
        super(SmallKeyRoom, self).__init__(doors)
        self.corpse = True
        self.corpse_item = 'small key'

    def enter(self, player):
        # Do special stuff for SmallKeyRoom in case of search
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(SmallKeyRoom, self).describe_room(self.came_from)
        # Print that there is a body in the room
        print(dedent("""
            As you step deeper into the room you notice a form in the corner. You are startled
            and take a quick step back, ready to get out of here, if need be. But as you take
            a more thorough look you notice that the form isn't moving.

            It seems like the body of a former adventurer who came in to seek fame and fortune
            in this infamous keep. It is a reminder of what could happen to you if you aren't
            careful.
        """))
        # If small key is found then continue as standard room
        return super(SmallKeyRoom, self).enter(player)
