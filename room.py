"""This class is for the possible rooms that a player can encounter"""
import numpy as np
import random
import action as act
from sys import exit
from textwrap import dedent
from monster import *

ACTION_DIRECTIONS = ['go north', 'go south', 'go west', 'go east', 'go back']
PROMPT = "\nWhat do you want to do? - > "

# Empty Room Actions
ER_ACTIONS = {
'show': act.ACTIONS_SHOW,
'go': act.ACTIONS_GO,
'open': act.ACTIONS_OPEN,
'search': act.ACTIONS_SEARCH,
'use': ['strength potion', 'health potion'],
'rest': []
}

ER_ACTION_MESSAGE = "You can't do that here. This is just an empty room."

# Monster Room actions before defeating Monster
MR_ACTIONS_PRE = {
'show': act.ACTIONS_SHOW,
'use': ['strength potion', 'health potion'],
'fight': None,
'attack': None,
'run': None,
'avoid': None
}

MR_ACTION_PRE_MESSAGE = "You are being attacked by a Monster. Focus on the fight!"

# Monster Room actions after defeating Monster
MR_ACTIONS_POST = ER_ACTIONS
MR_ACTION_POST_MESSAGE = ER_ACTION_MESSAGE

# Monster Room actions after avoiding Monster
MR_ACTIONS_AVOID = {
'show': act.ACTIONS_SHOW,
'go': act.ACTIONS_GO,
'use': ['strength potion', 'health potion']
}

MR_ACTION_AVOID_MESSAGE = "You just avoided the monster and he is hot on your tail. You don't have time to do that, just get out of the room!"

# Trap Room actions
TR_ACTIONS = ER_ACTIONS

TR_ACTION_MESSAGE = ER_ACTION_MESSAGE

# Obstacle Room Actions pre traversing obstacle
OR_ACTIONS_PRE = {
'traverse': act.ACTIONS_TRAVERSE,
'use': ['strength potion', 'health potion', 'rope'],
'show': ['map', 'item', 'name', 'type', 'action', 'stat'],
'go': ['back']
}

OR_ACTIONS_PRE_MESSAGE = "You can't do that here. You have to get across the debris field first."

# Obstacle Room Actions post traversing obstacle
OR_ACTIONS_POST = {
'go': act.ACTIONS_GO,
'show': act.ACTIONS_SHOW,
'use': ['strength potion', 'health potion']
}

OR_ACTION_POST_MESSAGE = "You can't do that here. The debris is dangerous, find an exit as soon as possible."

# Boss Room actions
BR_ACTIONS_PRE = {
'show': act.ACTIONS_SHOW,
'use': ['strength potion', 'health potion', 'boss key'],
'go': ['back']
}

BR_ACTION_PRE_MESSAGE = "You can't do that here. There is a big door in front of you!!"

BR_ACTIONS_POST = {
'show': ['map', 'item', 'name', 'type', 'action', 'stat'],
'use': ['strength potion', 'health potion'],
'fight': None,
'attack': None,
'run': None
}

BR_ACTION_POST_MESSAGE = "You are facing the Boss Monster of the Dungeon. Focus on the fight!"

# Monster Room actions after avoiding Monster
BR_ACTIONS_AVOID = MR_ACTIONS_AVOID

BR_ACTION_AVOID_MESSAGE = MR_ACTION_AVOID_MESSAGE

# Boss Key Room actions
BKR_ACTIONS = {
'show': act.ACTIONS_SHOW,
'go': act.ACTIONS_GO,
'search': act.ACTIONS_SEARCH,
'use': ['strength potion', 'health potion'],
'rest': None,
'open': ['chest']
}

BKR_ACTION_MESSAGE = ER_ACTION_MESSAGE

# Small Key Room actions
SKR_ACTIONS = ER_ACTIONS

SKR_ACTION_MESSAGE = ER_ACTION_MESSAGE

# Locked Room actions pre-open:
LR_ACTIONS_PRE = {
'show': ['map', 'item', 'name', 'type', 'action', 'stat'],
'go': ['back'],
'use': ['health potion', 'strength potion', 'small key'],
'open': ['door']
}

LR_ACTION_PRE_MESSAGE = "You can't do that here. There is a door in front of you."

# Locked Room actions post-open:
LR_ACTIONS_POST = ER_ACTIONS

LR_ACTION_POST_MESSAGE = ER_ACTION_MESSAGE

# Exit Room actions:
EXR_ACTIONS = {
'go': act.ACTIONS_GO,
'show': act.ACTIONS_SHOW,
'use': ['health potion', 'strength potion']
}

EXR_ACTION_MESSAGE = "This is the Exit Room. You can't do that here."

class Room:
    DIRECTIONS = ['North', 'South', 'West', 'East']
    EXIT_LOCATIONS = "As you entered the room you notice a passage to the "
    ITEMS = [[], 'health potion', 'strength potion', 'rope']
    P_ITEM = [0.8, 0.13, 0.05, 0.02]

    # doors is a boolean list of possible directions in same order as 'DIRECTIONS'
    # that means: doors = [False, True, True, False] indicates possible directions
    # as 'South' and 'West'. prev_dir must be
    def __init__(self, doors):
        # Randomly generate possible item in the room. Most likely there is nothing
        self.item = np.random.choice(self.ITEMS, 1, p = self.P_ITEM)[0]
        self.doors = doors
        self.monster = None
        self.monster_avoid = False
        self.obstacle = False
        self.trap = False
        self.chest = False
        self.chest_open =  False
        self.chest_item = []
        self.corpse = False
        self.corpse_item = []
        self.came_from = None
        self.door = False
        self.door_unlocked = False
        self.boss_door = False
        self.boss_door_unlocked = False
        # Gets the possible directions based on input when creating the room.
        self.directions = [self.DIRECTIONS[i] for i, x in enumerate(self.doors) if x]

    # Function that activates when Player enters room
    def enter(self, player, possible_actions = ER_ACTIONS, action_message = ER_ACTION_MESSAGE, passed_actions = ACTION_DIRECTIONS):
        # Gets the possible directions based on input when entering the room.
        self.directions = [self.DIRECTIONS[i] for i, x in enumerate(self.doors) if x]

        action = None

        # Get user action and keep going until directional action is found

        while action not in passed_actions:
            # Get action
            action = input(PROMPT)
            print('')

            # Interpret action and translate to standard action
            action = act.interpret_act(action)

            if action != None:

                # Check if action is allowed in this room
                if len(action.split()) == 1 and action in possible_actions.keys():
                    action_allowed = True
                elif len(action.split()) == 2 and action.split()[0] in possible_actions.keys() and action.split()[1] in possible_actions[action.split()[0]]:
                    action_allowed = True
                elif len(action.split()) == 3 and action.split()[0] in possible_actions.keys() and (action.split()[1] + ' ' + action.split()[2]) in possible_actions[action.split()[0]]:
                    action_allowed = True
                else:
                    action_allowed = False

                if action_allowed:
                # If action is understood and not directional
                    if action not in ACTION_DIRECTIONS:
                        # Perform standard action
                        player, action, self = act.perform_action(self, action, player, possible_actions)
                    elif action == 'go north':
                        next_pos = (player.position[0], player.position[1] - 1)
                    elif action == 'go south':
                        next_pos = (player.position[0], player.position[1] + 1)
                    elif action == 'go west':
                        next_pos = (player.position[0] - 1, player.position[1])
                    elif action == 'go east':
                        next_pos = (player.position[0] + 1, player.position[1])
                    elif action == 'go back':
                        next_pos = player.prev_pos

                    if action in ACTION_DIRECTIONS:
                        if player.map_data[next_pos[1]][next_pos[0]] == '-':
                            print("Can't go in that direction. There is a wall in the way.")
                            action = None
                else:
                    print(action_message)
                    action = None
            # Else
        else:
                # Continue looping for new input
                pass
        #
        if action in ACTION_DIRECTIONS:
            # Update player position based on (directional) action
            player.update_pos(next_pos[0], next_pos[1])

        # Return player.
        return player

    # Function that describes a standard room. Possible (visible) exits
    def describe_room(self, came_from):

        # Remove the direction Player came from, from directions
        # Since a Player will now where he came from there is no point in
        # printing that exit aas a possibility.

        if came_from in self.directions:
            self.directions.remove(came_from)
        else:
            pass

        # Print the direction the user came from (separate it from possible exits)
        # since Player will most likely want to go forward and not back.
        if came_from:
            print("After stumbling through a dark hallway you find yourself in another room")
            print("You came into the room from the %s wall" % came_from)
        else:
            print("This is the starting room. Lets start exploring the dungeon!\n")

        # Print different statements depending on the number of exits available.
        self.show_exits()

    def show_exits(self):

        if not self.directions:
            print("Seems like a dead end, the only exit is the one you came through")
        elif len(self.directions) == 1:
            print(self.EXIT_LOCATIONS + "%s"
                % self.directions[0])
        elif len(self.directions) == 2:
            print(self.EXIT_LOCATIONS + "%s and a passage to the %s"
                % (self.directions[0], self.directions[1]))
        else:
            print(self.EXIT_LOCATIONS + "%s, a passage to the %s and a passage to the %s"
                % (self.directions[0], self.directions[1], self.directions[2]))

    # Function calculates the direction the player came from when entering a room.
    def get_prev_dir(self, prev_pos, cur_pos):
        if prev_pos[0] > cur_pos[0]:
            return 'West'
        elif prev_pos[0] < cur_pos[0]:
            return 'East'
        elif prev_pos[1] < cur_pos[1]:
            return 'South'
        elif prev_pos[1] > cur_pos[1]:
            return 'North'
        else:
            return None


#test_room = TrapRoom([True, False, True, True])
#if test_room.monster:
#    print(test_room.monster.type)
#elif test_room.trap:
#    print(test_room.trap[0])
#else:
#    test_room.describe_room()

#if test_room.item:
#    print(test_room.item)
#else:
#    print("No item in room")
