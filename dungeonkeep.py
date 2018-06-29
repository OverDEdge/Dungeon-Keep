"""Game file where Dungeon-Keep is run"""
from map import *
import player as p
import numpy as np
import os
from os import path
from textwrap import dedent

PROMPT = '> '

class Engine:

    def __init__(self, game_map):

        self.game_map = game_map
        self.boss_defeated = False
        # Position is taken as an array where position [0][0] = y and [1][0] = x
        player_pos = np.where(self.game_map.map_data == 'P')
        player_name = input("Please enter Player Name: ")
        print(dedent("""
        Choose character from list:
        [1]. 'Paladin'
        Health: 100, Strength: 20, Defence: 15, Agility: 5
        [2]. 'Ranger'
        Health: 70, Strength: 15, Defence: 10, Agility: 15
        [3]. 'Thief'
        Health: 60, Strength: 10, Defence: 10, Agility: 20
        [4]. 'Sorcerer'
        Health: 75, Strength: 15, Defence: 10, Agility: 10
        """))

        chosen = False
        while not chosen:
            chosen = True
            player_character = input("Please enter Player Character: ")
            self.player1 = None
            if player_character.lower() == 'paladin' or player_character == '1':
                self.player1 = p.Paladin(player_pos[1][0], player_pos[0][0], player_name, self.game_map.map_data)
            elif player_character.lower() == 'ranger' or player_character == '2':
                self.player1 = p.Ranger(player_pos[1][0], player_pos[0][0], player_name, self.game_map.map_data)
            elif player_character.lower() == 'thief' or player_character == '3':
                self.player1 = p.Thief(player_pos[1][0], player_pos[0][0], player_name, self.game_map.map_data)
            elif player_character.lower() == 'sorcerer' or player_character == '4':
                self.player1 = p.Sorcerer(player_pos[1][0], player_pos[0][0], player_name, self.game_map.map_data)
            else:
                print("Choose character from list. Enter number or character type.")
                chosen = False

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')
# Load dungeon map from game directory
map_file = 'normal_map.txt'
game_folder = path.dirname(__file__)
filename = path.join(game_folder, map_file)
map = Map(filename)

# Initialize Game Engine
game_engine = Engine(map)

#print(map.map_rooms2[game_engine.player1.position[1]][game_engine.player1.position[0]])

# Print Welcome text
print(dedent("""
Welcome to Dungeon-Keep. You have entered the keep in search of the great
treasure which is said to lie hidden within. But beware, dangers can be
found around every corner and no one has yet to return from the depths
of the keep. Good luck dear hero!
"""))

# Add map_data to player to display as player finds map

#print(game_engine.player1.map_data)

#print(map.map_rooms[game_engine.player1.position[1] * map.tilewidth + game_engine.player1.position[0]])

while True:
    #print(game_engine.player1.map_data)
    #game_engine.player1 = map.map_rooms[game_engine.player1.position[1] * map.tilewidth + game_engine.player1.position[0]].enter(game_engine.player1)
    game_engine.player1 = map.map_rooms[game_engine.player1.position[1]][game_engine.player1.position[0]].enter(game_engine.player1)
