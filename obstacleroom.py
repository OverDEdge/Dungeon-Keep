"""Obstacle Room class"""
from room import *

class ObstacleRoom(Room):
    def __init__(self, doors):
        super(ObstacleRoom, self).__init__(doors)
        self.rope = False

    def enter(self, player):
        # Do special stuff for ObstacleRoom
        print(dedent("""
        As you enter the room you notice a field of debris all across the floor.
        The spikes and spears littered everywhere makes this a treacherous crossing.
        All you can do here is try to traverse this obstacle.
        """))

        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)

        # Save current position to check after asking for action
        old_pos = player.position
        player =  super(ObstacleRoom, self).enter(player, OR_ACTIONS_PRE, OR_ACTIONS_PRE_MESSAGE,
                    ['traverse obstacle', 'use rope', 'go back'])

        # If position has changed then player has chosen 'go back' and should return new player
        if old_pos == player.position:
            return super(ObstacleRoom, self).enter(player, OR_ACTIONS_POST, OR_ACTION_POST_MESSAGE)
        else:
            return player



    def describe_room(self, came_from):
        super(ObstacleRoom, self).describe_room(came_from)
