"""This class is for the possible rooms that a player can encounter"""
import numpy as np
import random
from sys import exit
from textwrap import dedent
from monster import *

ACTION_DIRECTIONS = ['go north', 'go south', 'go west', 'go east']
PROMPT = "> "

class Room:
    DIRECTIONS = ['North', 'South', 'West', 'East']
    DOOR_LOCATIONS = "As you enter the room you notice a door to the "
    ITEMS = [[], 'Health Potion', 'Strength Potion', 'Rope']
    P_ITEM = [0.8, 0.13, 0.05, 0.02]
    TRAPS = {'Roof falls down': 5, 'Trap door': 10, 'Arrows from wall': 15}
    P_TRAP = [0.7, 0.2, 0.1]
    # doors is a boolean list of possible directions in same order as 'DIRECTIONS'
    # that means: doors = [False, True, True, False] indicates possible directions
    # as 'South' and 'West'. prev_dir must be
    def __init__(self, doors):
        # Randomly generate possible item in the room. Most likely there is nothing
        self.item = np.random.choice(self.ITEMS, 1, p = self.P_ITEM)
        self.doors = doors
        #self.prev_dir = prev_dir
        self.monster = None
        self.obstacle = None
        self.trap = None

    # Function that activates when Player enters room
    def enter(self, player):
        # Get previous direction of player
        came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        self.describe_room(came_from)

        # Get user action and keep going until directional action is found
        action = None
        while action not in ACTION_DIRECTIONS:
            # Get action
            print("What do you want to do?")
            action = input(PROMPT)

            # Interpret action and translate to standard action

            # If action is understood
                # Perform standard action
            # Else
                # Write out error message since input was not understood
            pass

        # Update player position based on (directional) action
        if action == 'go north':
            player.update_pos(player.position[0], player.position[1] - 1)
        elif action == 'go south':
            player.update_pos(player.position[0], player.position[1] + 1)
        elif action == 'go west':
            player.update_pos(player.position[0] - 1, player.position[1])
        else:
            player.update_pos(player.position[0] + 1, player.position[1])

        # Return player.
        return player

    # Function that describes a standard room. Possible (visible) exits
    def describe_room(self, came_from):
        # Gets the possible directions based on input when creating the room.
        self.directions = [self.DIRECTIONS[i] for i, x in enumerate(self.doors) if x]

        # Remove the direction Player came from, from directions
        # Since a Player will now where he came from there is no point in
        # printing that exit aas a possibility.

        if came_from in self.directions:
            self.directions.remove(self.prev_dir)
        else:
            pass

        # Print the direction the user came from (separate it from possible exits)
        # since Player will most likely want to go forward and not back.
        if came_from:
            print("You come into the room from the %s wall" % came_from)
        else:
            print("This is the starting room")

        # Print different statements depending on the number of exits available.
        if not self.directions:
            print("Seems like a dead end, the only door is the one you came through")
        elif len(self.directions) == 1:
            print(self.DOOR_LOCATIONS + "%s"
                % self.directions[0])
        elif len(self.directions) == 2:
            print(self.DOOR_LOCATIONS + "%s and a door to the %s"
                % (self.directions[0], self.directions[1]))
        else:
            print(self.DOOR_LOCATIONS + "%s, a door to the %s and a door to the %s"
                % (self.directions[0], self.directions[1], self.directions[2]))

    def get_prev_dir(self, prev_pos, cur_pos):
        if prev_pos[0] < cur_pos[0]:
            return 'West'
        elif prev_pos[0] > cur_pos[0]:
            return 'East'
        elif prev_pos[1] < cur_pos[1]:
            return 'North'
        elif prev_pos[1] > cur_pos[1]:
            return 'South'
        else:
            return None

# EmptyRoom is basically the standard room.

class EmptyRoom(Room):

    def __init__(self, doors):
        super(EmptyRoom, self).__init__(doors)

    def enter(self, player):
        super(EmptyRoom, self).enter(player)

class MonsterRoom(Room):
    def __init__(self, doors):
        super(MonsterRoom, self).__init__(doors)
        # Generate a random monster for this room
        self.monster = Monster(random.choice(list(MONSTER_STATS.keys())))

    # Function that activates when Player enters room
    def enter(self, player):
        # Check if monster has been defeated or not
        if self.monster:
            # Print appropriate monster text
            if self.monster.type == 'Skeleton':
                print(dedent("""
                    As you step through to the next room you hear a strange rattling noice
                    coming from behind the door. Acting on pure instinct you manage to
                    avoid the swinging blade coming from the side.
                    As you turn to face your opponent you find yourself face to face with
                    a walking Skeleton holding a broadsword.
                """))
            elif self.monster.type == 'Goblin':
                print(dedent("""
                    Entering the room you see a small green form barreling toward you at
                    high speed. You dive to the side to avoid getting speared through
                    the abdomen. The creature barrels into the spot you were just
                    occupying giving a mightly snarl. It soon recovers and faces you with
                    a spear in hand. There is no mistaking those ugly features, a Goblin
                    now blocks your way
                """))
            elif self.monster.type == 'Dark Elf':
                print(dedent("""
                    You enter the room and close the door behind you since don't want
                    anyone sneaking up on you from the back. As you turn around you
                    suddenly hear a high pitched screech coming from a dark corner. Out
                    strolls a small evil Looking creature with sharp teeth. Great, you
                    just stepped into the territory of a Dark Elf.
                    """))
            else:
                print("Monster type not defined. Something has gone wrong. Exiting game.")
                exit(1)

            # Start fight sequence
        else:
            pass

        # If monster is gone continue as standard room
        super(MonsterRoom, self).enter(player)
        # Get previous direction of player
        #came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room descrition
        #self.describe_room(came_from)

        # Ask for player action
        # Keep going until action to leave room is detected

class TrapRoom(Room):
    def __init__(self, doors):
        super(TrapRoom, self).__init__(doors)
        # Generate a random trap
        self.trap = np.random.choice(list(self.TRAPS.keys()), 1, p = self.P_TRAP)
        # Print appropriate text

    def enter(self, player):
        if self.trap:
            if self.trap == 'Roof falls down':
                print(dedent("""
                    As soon as you step into the room debris start to rain down from above.
                    You dive for the corner but can't fully avoid the falling boulders.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            elif self.trap == 'Trap door':
                print(dedent("""
                    You take a few steps into the seemingly empty room. But on your third
                    step the ground opens up beneath you revealing a spiked floor.
                    Thanks to luck and the decrepit conditions of the spikes you are not
                    fully impaled, but you still take some damage.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            elif self.trap == 'Arrows from wall':
                print(dedent("""
                    As you survey the room you feel one of the tiles dip slightly under
                    your foot. You know this doesn't bode well and as soon as that
                    thought passes through your head, arrows start shooting out of the
                    nearby walls. You tuck and roll to escape the flying missiles but
                    a few still manage to find its mark.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            else:
                print("Trap type isn't defined. Something has gone wrong. Exiting game")
                exit(1)
        else:
            pass

        # If trap is gone continue as standard room
        super(TrapRoom, self).enter(player)

        #self.describe_room()
        # Get previous direction of player
        #came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room descrition
        #self.describe_room(came_from)


class ObstacleRoom(Room):
    def __init__(self, doors):
        super(ObstacleRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for ObstacleRoom
        pass
        # If obstacle is passed can only choose exit, not search.

class BossRoom(Room):

    def __init__(self, doors):
        super(BossRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for BossRoom
        pass
        # If boss is passed defeated game ends

class SecretRoom(Room):
    def __init__(self, doors):
        super(SecretRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for SecretRoom in case of search

        # If secret is found then continue as standard room
        super(SecretRoom, self).enter(player)

class LockedRoom(Room):
    def __init__(self, doors):
        super(LockedRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for LockedRoom in case of search

        # If unlocked room then continue as standard room
        super(LockedRoom, self).enter(player)

class SmallKeyRoom(Room):
    def __init__(self, doors):
        super(SmallKeyRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for SmallKeyRoom in case of search

        # If small key is found then continue as standard room
        super(SmallKeyRoom, self).enter(player)

class BossKeyRoom(Room):
    def __init__(self, doors):
        super(BossKeyRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for BossKeyRoom in case of search

        # If boss key is found then continue as standard room
        super(BossKeyRoom, self).enter(player)

class MapRoom(Room):
    def __init__(self, doors):
        super(MapRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for MapRoom in case of search

        # If map is found then continue as standard room
        super(MapRoom, self).enter(player)

class ExitRoom(Room):
    def __init__(self, doors):
        super(ExitRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for ExitRoom -> End Game
        pass

class PlayerRoom(Room):
    def __init__(self, doors):
        super(PlayerRoom, self).__init__(doors)

    def enter(self, player):
        # Do special stuff for PlayerRoom
        print(dedent("""
        Welcome to Dungeon-Keep. You have entered the keep in search of the great
        treasure which is said to lie hidden within. But beware, dangers can be
        found around every corner and no one has yet to return from the depths
        of the keep. Good luck dear hero!
        """))
        # Then continue as standard room
        super(PlayerRoom, self).enter(player)


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
