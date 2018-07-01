"""Locked Room class"""

from room import *

class LockedRoom(Room):
    def __init__(self, doors):
        super(LockedRoom, self).__init__(doors)
        self.door = True

    def enter(self, player):
        # Do special stuff for LockedRoom in case of search
        # Do special stuff for BossRoom
        print(dedent("""
        As you stumble along the corridor you are notice a wooden door up ahead.
        It has a keyhole and a handle. What could be on the other side?
        """))
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Save current position to check after asking for action
        old_pos = player.position
        player =  super(LockedRoom, self).enter(player, LR_ACTIONS_PRE, LR_ACTION_PRE_MESSAGE,
                    ['open door', 'go back'])
        # If unlocked room then continue as standard room

        # If position has changed then player has chosen 'go back' and should return new player
        if old_pos == player.position:
            # Show room description
            super(LockedRoom, self).describe_room(self.came_from)
            return super(LockedRoom, self).enter(player, LR_ACTIONS_POST, LR_ACTION_POST_MESSAGE)
        else:
            return player
