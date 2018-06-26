"""This class is for an empty room with some standard actions"""
from room import *

class Room:
    DIRECTIONS = ['North', 'South', 'West', 'East']
    DOOR_LOCATIONS = "As you enter the room you notice a door to the "

    def __init__(self, doors, prev_dir):
        self.item = []
        self.doors = doors
        self.prev_dir = prev_dir

    def describe_room(self):
        self.directions = [self.DIRECTIONS[i] for i, x in enumerate(self.doors) if x]
        self.directions.remove(self.prev_dir)
        print("You come into the room from the %s wall" % self.prev_dir)
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

class EmptyRoom(Room):
    pass

#test_room = Room([True, False, True, True], 'North')
#test_room.describe_room()
