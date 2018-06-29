"""This will contain methods for understanding and performing user actions"""
from sys import exit
import random
from textwrap import dedent

ACTIONS_SHOW = ['map', 'item', 'name', 'type', 'action', 'exit', 'stat']
ACTIONS_GO = ['north', 'south', 'west', 'east', 'back']
ACTIONS_SEARCH = ['room', 'chest', 'corpse', 'body']
ACTIONS_OPEN = ['chest', 'door']
ACTIONS_TRAVERSE = ['obstacle']
ACTIONS_SWING = ['rope']
ACTIONS_USE = ['health potion', 'strength potion', 'small key', 'boss key']

POSSIBLE_ACTIONS_2_WORDS = {
'show': ACTIONS_SHOW,
'go': ACTIONS_GO,
'search': ACTIONS_SEARCH,
'open': ACTIONS_OPEN,
'traverse': ACTIONS_TRAVERSE,
'swing': ACTIONS_SWING
}

POSSIBLE_ACTIONS_3_WORDS = {
'use': ACTIONS_USE
}

POSSIBLE_ACTIONS_1_WORD = ['rest', 'fight', 'run', 'avoid']

def interpret_act(action):

    if action:
        action = action.lower()
        action_words = action.split()

        # Check first word in action and if it is a 2 word action or 1 word action
        if action_words[0] in list(POSSIBLE_ACTIONS_2_WORDS.keys()):
            if len(action_words) > 1:
                return get_second_action(action_words[0:2], POSSIBLE_ACTIONS_2_WORDS[action_words[0]])
            else:
                print(f"For '{action_words[0]}' please use specifier from:\n {POSSIBLE_ACTIONS_2_WORDS[action_words[0]]}")
                return None
        elif action_words[0] in POSSIBLE_ACTIONS_1_WORD:
            return action_words[0]
        elif action_words[0] in list(POSSIBLE_ACTIONS_3_WORDS.keys()):
            if len(action_words) > 2:
                comb_action_word = action_words[1] + ' ' + action_words[2]
                return get_second_action([action_words[0], comb_action_word], POSSIBLE_ACTIONS_3_WORDS[action_words[0]])
            else:
                print(f"For '{action_words[0]}' please use specifier from:\n {POSSIBLE_ACTIONS_3_WORDS[action_words[0]]}")
                return None
        else:
            print("Action: '%s' not understood. Please retry" % action)
            return None
    else:
        return None

def get_second_action(action_words, pos_actions):
    # Check if second word ends with 's'. If that is the case, remove the 's'
    if action_words[1][-1] == 's':
        action_words[1] = action_words[1][:-1]
    else:
        pass

    for action in pos_actions:
        if action_words[1] == action:
            return action_words[0] + ' ' + action_words[1]
        else:
            pass

    print(f"For '{action_words[0]}' please use specifier from:\n {pos_actions}")
    return None

def perform_action(room, action, player, possible_actions):
    if action == 'show map':
        if 'map' in player.items:
            print(player.map_data)
            print("'P' = Your position")
            print("'E' = Exit room")
            print("'x' = Unvisited rooms")
            print("'o' = Visited rooms")
        else:
            print("You don't have a map of this place yet. Better find one!")
    elif action == 'show item':
        print(f"You currently have the following items in you bag:\n {player.items}")
    elif action == 'show name':
        print(f"Have you forgotten your name?! It is '{player.name}'")
    elif action == 'show type':
        print(f"How could you forget that you are a '{player.type}'")
    elif action == 'show action':
        print("The possible actions in the room can be found below.")
        print("Depending on the content of the room and available player items")
        print("all actions might not work.\n")
        for word1 in list(possible_actions.keys()):
            if word1 in POSSIBLE_ACTIONS_2_WORDS.keys() or word1 in POSSIBLE_ACTIONS_3_WORDS.keys():
                for word2 in possible_actions[word1]:
                    print(f"'{word1} {word2}'")

            if word1 in POSSIBLE_ACTIONS_1_WORD:
                print(f"'{word1}'")

    elif action == 'show exit':
        if room.came_from:
            print("You come into the room from the %s wall" % room.came_from)
        else:
            pass
        room.show_exits()
    elif action == 'show stat':
        print("Your current stats are:")
        print(f"Health: {player.health}\nAttack: {player.attack}\nDefence: {player.defence}\nAgility: {player.agility}")
    elif action == 'search room':
        print("You take your time and search the room for any possible treasure.")
        if len(room.item) > 0:
            print("You are in luck. Hidden in a crevice in the wall you find a %s"
                    % room.item)
            player.items.append(room.item.lower())
            room.item = []
        else:
            print("After a thorough search you conclude that there is nothing more of interest in the room")
    elif action == 'search corpse' or action == 'search body':
        if room.corpse and len(room.corpse_item) > 0:
            print("You figure you need every tool possible to survive this place so you decide to search the body of the fallen warrior.")
            print("Hidden in a breast pocket you find a %s", room.corpse_item)
            player.item = room.corpse_item
            room.corpse_item = []
        elif room.corpse and len(room.corpse_item) == 0:
            print("You have already searched the body. No point doing it again")
        else:
            print("You can't do that here, there is no corpse/body in the room")
    elif action == 'search chest' and room.chest_open and room.chest:
        if room.chest and len(room.chest_item) > 0:
            print("As you peek into the open the chest you notice something inside and you pick it up. You have gained a %s", room.chest_item)
            player.item = room.chest_item
            room.chest_item = []
        elif room.chest and len(room.chest_item) == 0:
            print("You have already searched the chest. No point looking in there again!")
        else:
            print("Something is wrong. Chest exist in room and is open but can't get item. Exiting game.")
            exit(1)
    elif action == 'search_chest' and room.chest and not room.chest_open:
        print("You can't search the chest since it is still closed.")
    elif action == 'open_chest' and room.chest:
        print("The big golden chest fills up your vision. You step forward, grab hold and slowly lift the lid. You notice a shine coming from inside. The chest is now open")
        room.chest_open = True
    elif (action == 'open chest' and not room.chest) or (action == 'search chest' and not room.chest):
        print("You can't do that here, there is no chest in this room")
    elif action == 'open door' and room.door:
        pass
        if room.door_unlocked:
            print("You grab hold of the handle and push on the door. The hinges creak but with a little bit more strength the door starts to slide open. You take a deep breath and enter the passage beyond.")
        else:
            print("You take hold of the handle and push with all your might. The door is not budging, it must be locked. I wonder if I need a key of some sort?")
    elif action == 'open door' and room.boss_door:
        pass
        if room.boss_door_unlocked:
            print("The massive doors loom before you. You know something big msut be waiting for you enside. Despite your fear, you gather your strength and slowly inch the massive gate open. It makes a horrible screeshing noice as it starts to open. You slip into the small opening and hear the gate slam shut behind you. Only way now is forward into the dark.")
        else:
            print("You take hold of the massive handle and push with all your might. The door is not budging, at first you think it might eb too heavy but you notice a key hole on the door so it might be locked. I wonder if I need a special key of some sort?")
    elif action == 'open door' and not room.door and not room.boss_door:
        print("You can't do that here, there is no door to open.")
    elif action == 'traverse obstacle':
        if random.randint(0, 30) > player.agility:
            action = None
            print(dedent("""
            You slip on a piece of loose debris and loose you balance.
            In the fall you get pierced by some sharp protruding object.
            """))
            print("\nYou loose 5 Health points.\n")
            player.health -= 5
            print("Current Health: %s\n" % player.health)
        else:
            print(dedent("""
            You manage to traverse the obstacle and you are free to exit the room.
            """))
    elif action == 'swing rope' and 'rope' in player.items:
        print("You use the rope to safely traverse the obstacle.\n")
    elif action == 'swing rope' and 'rope' not in player.items:
        action = None
        print("You don't have any rope.\n")
    elif action == 'use health potion' and  'health potion' in player.items:
        print("You eye the reddish hue of the fluid inside the vial and decide to chug it all at once. 'Hmmm, it tastes like raspberry juice'")
        player.health = min(player.health + 20, player.maxhealth)
        print("You feel rejuvenated and your health is: %d" % player.health)
    elif action == 'use health potion' and 'health potion' not in player.items:
        print("You don't have any health potions in your bag.")
    elif action == 'use strength potion' and 'strength potion' in player.items:
        print("You swallow the green liquid before you have time to think better of it. It doesn't take long before you start to feel stronger")
        player.attack += 5
        print("Your new attack is: %d" % player.attack)
    elif action == 'use strength potion' and 'strength potion' not in player.items:
        print("You don't have any strength potions in your bag.")


    return player, action, room
