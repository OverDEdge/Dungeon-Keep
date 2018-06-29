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

        rope = False

        action = ''
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        #print(('go' + ' ' + self.came_from).lower())

        while action != 'traverse obstacle' and action != ('go' + ' ' + self.came_from).lower() and not rope:

            # Get action
            action = input(PROMPT)
            # Interpret action and translate to standard action
            action = act.interpret_act(action)

            # Check if player can traverse obstacle
            if action == 'traverse obstacle':
                if random.randint(0, 30) > player.agility:
                    action = None
                    print(dedent("""
                    You slip on a piece of loose debris and loose you balance.
                    In the fall you get pierced by some sharp protruding object.
                    """))
                    print("\nYou loose 5 Health points.\n")
                    player.health -= 10
                    print("Current Health: %s\n" % player.health)
                else:
                    print(dedent("""
                    You manage to traverse the obstacle and you are free to exit the room.
                    """))
            elif action == ('go' + ' ' + self.came_from).lower():
                pass
            elif action == 'use rope' and 'rope' in player.items:
                rope = True
            else:
                print("You can't do anything until you get past this debris!")


        # If obstacle is passed can only choose to exit room, not search.
        if action == 'traverse obstacle':
            return super(ObstacleRoom, self).enter(player, OR_ACTIONS_POST, OR_ACTIONS_POST_MESSAGE)
        elif action == 'go north':
            next_pos = (player.position[0], player.position[1] - 1)
        elif action == 'go south':
            next_pos = (player.position[0], player.position[1] + 1)
        elif action == 'go west':
            next_pos = (player.position[0] - 1, player.position[1])
        elif action == 'go east':
            next_pos = (player.position[0] + 1, player.position[1])
        if not rope:
            player.update_pos(next_pos[0], next_pos[1])
            print("You choose to skip the obstacle and turn back to the previous room\n")
            return player
        else:
            print("You use the rope to safely traverse the obstacle.\n")

            return super(ObstacleRoom, self).enter(player, OR_ACTIONS_POST, OR_ACTIONS_POST_MESSAGE)



    def describe_room(self, came_from):
        super(ObstacleRoom, self).describe_room(came_from)
