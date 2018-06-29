"""This class is for the map of the dungeon that the player has to traverse
The map should be initialized from a text file and depending on the position
of the Player the map should load the appropriate room.

Text file MUST have walls = '-' all around the edges. This is to avoid
looking out of bounds.

OK Map (only '-' are at edge of map):
-----
-Bxx-
--P--
--E--
-----

NOK Map (Both 'B', 'E' and two 'x' rooms are next to the edge):
-Bxx-
--P--
--E--

List of possible rooms:
'-' = None (This is wall and not possible to enter)
'x' = EmptyRoom()
'T' = TrapRoom() (one time trap)
'O' = ObstacleRoom() (permanent)
'M' = MonsterRoom()
'B' = BossRoom() (requires Boss key)
'S' = SecretRoom() (hidden room only seen if adjacent room is searched)
'L' = LockedRoom() (requires small key)
'k' = SmallKeyRoom() (looks like Empty Room but contains a small key)
'K' = BossKeyRoom() (contains a chest with Boss key)
'm' = MapRoom() (contains a chest with map of dungeon)
'E' = ExitRoom() (exit out of dungeon (ends the game)
'P' = PlayerRoom() (Player start position)
"""

from bossroom import *
from bosskeyroom import *
from emptyroom import *
from exitroom import *
from lockedroom import *
from maproom import *
from monsterroom import *
from obstacleroom import *
from playerroom import *
from secretroom import *
from smallkeyroom import *
from traproom import *

# Anonymous 'Constant' that take x as input to initialize the rooms
POSSIBLE_ROOMS = lambda x: {
'-': None,
'x': EmptyRoom(x),
'T': TrapRoom(x),
'O': ObstacleRoom(x),
'M': MonsterRoom(x),
'B': BossRoom(x),
'S': SecretRoom(x),
'L': LockedRoom(x),
'k': SmallKeyRoom(x),
'K': BossKeyRoom(x),
'm': MapRoom(x),
'E': ExitRoom(x),
'P': PlayerRoom(x)
}

import numpy as np

class Map():

    def __init__(self, map_file = 'normal_map.txt'):
        map_data = []
        # Read map data from file
        with open(map_file, 'rt') as f:
            for line in f:
                map_data.append(line.strip())

        self.tilewidth = len(map_data[0])
        self.tileheight = len(map_data)
        # Array of Room Objects where walls are None
        #self.map_rooms = np.empty([self.tileheight, self.tilewidth],
        #                            dtype = 'str')
        #self.map_rooms = []
        # Array of map data to be accesible by player after getting map.
        self.map_data = np.empty([self.tileheight, self.tilewidth],
                                    dtype = 'str')
        self.map_rooms = np.empty([self.tileheight, self.tilewidth],
                                    dtype = 'object')

        # Row becomes the y direction and col becomes the x direction. Where:
        # Decreasing y = 'North', Increasing y = 'South'
        # Decreasing x = 'West', Increasing x = 'East'
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):

                # Only show possible path for player and not content of map
                if tile == 'x' or tile == '-' or tile == 'E' or tile == 'P':
                    self.map_data[row][col] = tile
                else:
                    self.map_data[row][col] = 'x'

        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):

                # Initialize as all possible directions
                pos_dir = [True, True, True, True]
                # No point in calculating possible paths for walls
                # since they will be None objects and Exit will initiate
                # end of game
                if tile != '-':
                    pos_dir = self.possible_directions(row, col, pos_dir)
                else:
                    pass
                # Initialize correct rooms
                self.map_rooms[row][col] = POSSIBLE_ROOMS(pos_dir)[tile]
                #self.map_rooms.append(POSSIBLE_ROOMS(pos_dir)[tile])
                #if POSSIBLE_ROOMS(pos_dir)[tile]:
                    #print(POSSIBLE_ROOMS(pos_dir)[tile].item)

        #print(self.map_data)
        #print("Tilewidth:", self.tilewidth)
        #print("Tileheight:", self.tileheight)
        # Player Room on Normal map
        #print(self.map_rooms[7*self.tilewidth + 5])

    # Funtion that checks neighbouring rooms and returns a boolean array of
    # available directions according to: ['North', 'South', 'West', 'East']
    # [True, True, False, True] means possible directions are:
    # ['North', 'South', 'West']
    def possible_directions(self, row, col, pos_dir):

        if self.map_data[row - 1][col] == '-':
            pos_dir[0] = False
        else:
            pass

        if self.map_data[row + 1][col] == '-':
            pos_dir[1] = False
        else:
            pass

        if self.map_data[row][col - 1] == '-':
            pos_dir[2] = False
        else:
            pass

        if self.map_data[row][col + 1] == '-':
            pos_dir[3] = False
        else:
            pass

        return pos_dir

map = Map()
