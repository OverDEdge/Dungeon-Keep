"""This will contain methods for understanding and performing user actions"""
from sys import exit
import random
import math
from textwrap import dedent

MAX_AGILITY = 40
MAX_ATTACK = 40
MAX_DEFENCE = 40

ACTIONS_SHOW = ['map', 'item', 'name', 'type', 'action', 'exit', 'stat']
ACTIONS_GO = ['north', 'south', 'west', 'east', 'back']
ACTIONS_SEARCH = ['room', 'chest', 'corpse', 'body']
ACTIONS_OPEN = ['chest', 'door']
ACTIONS_TRAVERSE = ['obstacle']
ACTIONS_ROPE = ['rope']
ACTIONS_USE = ['health potion', 'strength potion', 'small key', 'boss key']

POSSIBLE_ACTIONS_2_WORDS = {
'show': ACTIONS_SHOW,
'go': ACTIONS_GO,
'search': ACTIONS_SEARCH,
'open': ACTIONS_OPEN,
'traverse': ACTIONS_TRAVERSE,
'use': ACTIONS_ROPE
}

POSSIBLE_ACTIONS_3_WORDS = {
'use': ACTIONS_USE
}

POSSIBLE_ACTIONS_1_WORD = ['rest', 'fight', 'attack', 'run', 'avoid']

def interpret_act(action):

    if action:
        action = action.lower()
        action_words = action.split()

        # Check first word in action and if it is a 2 word action or 1 word action
        if action_words[0] in list(POSSIBLE_ACTIONS_2_WORDS.keys()) and len(action_words) < 3:
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
            print("You came into the room from the %s wall" % room.came_from)
            room.directions.remove(room.came_from)
        else:
            pass
        room.show_exits()

    elif action == 'show stat':
        print("Your current stats are:")
        print(f"Health: {player.health}\nAttack: {player.attack}\nDefence: {player.defence}\nAgility: {player.agility}")

    elif action == 'search room':
        print("You take your time and search the room for any possible treasure.")
        if len(room.item) > 0:
            print("You are in luck. Hidden in a crevice in the wall you find '%s'"
                    % room.item)
            player.items.append(room.item)
            room.item = []
            # Check if found item was a legendary item
            if 'cloak of mobility' in player.items:
                print(dedent("""
                The have attained the legendary cape: 'Cloak of Mobility'. The cloak will help you
                overcome obstacles and avoid dangers by boosting your movement.
                """))
                player.agility += 10
                print("Your Agility is now: %d" % player.agility)
                if player.type == 'Thief':
                    print(dedent("""
                    Only a Thief like you know how to unlock the cloaks full potential. A combination of
                    agility and misdirection increases your defence ability in fights.
                    """))
                    player.defence += 10
                    print("Your Agility is now: %d" % player.defence)
            elif 'mjolnir' in player.items and player.attack >= MAX_ATTACK - 20:
                print(dedent("""
                You have attained the legendary weapon: 'Mjolnir'. Only a true warrior with the
                strength of five men could wield this weapon. It boost both your attack and
                defence even further.
                """))
                player.attack += 10
                player.defence += 5
                print("Your Attack is now: %d" % player.attack)
                print("Your Defence is now: %d" % player.defence)
            elif 'mjolnir' in player.items and player.attack < MAX_ATTACK - 20:
                print("You are not strong enough to pick up Mjolnir")
                print("This heavy hammer requires an attack strength of %d to lift" % (MAX_ATTACK - 20))
                room.item = 'mjolnir'
            elif 'elder wand' in player.items and player.type == 'Sorcerer':
                print(dedent("""
                You have attained the legendary weapon: 'Elder Wand'. Only a geniune Sorcerer of the
                highest order could wield this weapon. It boost both your attack and defence to
                immesurable heights.
                """))
                player.attack += 10
                player.defence += 10
                print("Your Attack is now: %d" % player.attack)
                print("Your Defence is now: %d" % player.defence)
            elif 'elder wand' in player.items and player.type != 'Sorcerer':
                print("Only a Sorcerer may wield the 'Elder Wand'. You will have to leave it behind.")
                room.item = 'elder wand'
            elif 'bow of tell' in player.items and player.type == 'Ranger':
                print(dedent("""
                You have attained the legendary weapon: 'Bow of Tell'. This bow used to belong to Wilhelm
                Tell and only a master sharpshooter can wield its power.
                """))
                player.attack += 10
                player.agility += 10
                print("Your Attack is now: %d" % player.attack)
                print("Your Agility is now: %d" % player.agility)
            elif 'bow of tell' in player.items and player.type != 'Ranger':
                print("Only a Ranger may wield the 'Bow of Tell'. You will have to leave it behind.")
                room.item = 'bow of tell'
        else:
            print("After a thorough search you conclude that there is nothing more of interest in the room")

    elif action == 'search corpse' or action == 'search body':
        if room.corpse and len(room.corpse_item) > 0:
            print(dedent("""
            You figure you need every tool possible to survive this place so you decide
            to search the body of the fallen warrior.
            """))
            print("Hidden in a breast pocket you find '%s'" % room.corpse_item)
            player.items.append(room.corpse_item)
            room.corpse_item = []
        elif room.corpse and len(room.corpse_item) == 0:
            print("You have already searched the body. No point doing it again")
            action = None
        else:
            print("You can't do that here, there is no corpse/body in the room")
            action = None

    elif action == 'search chest':
        if room.chest and len(room.chest_item) > 0 and room.chest_open:
            print("As you peek into the open the chest you notice something inside and you pick it up.")
            print("You have gained a %s" % room.chest_item)
            player.items.append(room.chest_item)
            room.chest_item = []
        elif room.chest and len(room.chest_item) == 0:
            print("You have already searched the chest. No point looking in there again!")
            action = None
        elif room.chest and not room.chest_open:
            print("You can't search the chest since it is still closed.")
            actin = None
        else:
            print("You can't do that here, there is no chest in this room")
            action = None

    elif action == 'open chest':
        if room.chest and not room.chest_open:
            print(dedent("""
            The big golden chest fills up your vision. You step forward, grab hold and slowly
            lift the lid. You notice a shine coming from inside. The chest is now open!
            """))
            room.chest_open = True
        elif room.chest and room.chest_open:
            print("You can't really do that since the chest is already open.")
            action = None
        else:
            print("You can't do that here, there is no chest in this room")
            action = None

    elif action == 'open door':
        if room.door:
            if room.door_unlocked:
                print(dedent("""
                You grab hold of the handle and push on the door. The hinges
                creak but with a little bit more strength the door starts to slide open. You
                take a deep breath and enter the passage beyond.
                """))
            else:
                print(dedent("""
                You take hold of the handle and push with all your might. The door is not
                budging, it must be locked. I wonder if I need a key of some sort?
                """))
                action = None
        elif room.boss_door:
            if room.boss_door_unlocked:
                print(dedent("""
                The massive doors loom before you. You know something big must be waiting for you
                inside. Despite your fear, you gather your strength and slowly inch the massive
                gate open. It makes a horrible screeshing noice as it starts to open. You slip into
                the small opening and hear the gate slam shut behind you. Only way now is forward
                into the dark.
                """))
            else:
                print(dedent("""
                You take hold of the massive handle and push with all your might. The door is not
                budging, at first you think it might be too heavy but you notice a key hole on the
                door so it might be locked. I wonder if I need a special key of some sort?
                """))
                action = None
        else:
            print("You can't do that here, there is no door to open.\n")
            action = None

    elif action == 'traverse obstacle':
        if random.randint(0, MAX_AGILITY - 10) > player.agility:
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

    elif action == 'use rope':
        if 'rope' in player.items:
            print("You use the rope across the divide to safely traverse the obstacle.")
        elif 'rope' not in player.items:
            action = None
            print("You don't have any rope.\n")

    elif action == 'use health potion':
        if 'health potion' in player.items:
            print(dedent("""
            You eye the reddish hue of the fluid inside the vial and decide to chug it
            all at once. 'Hmmm, it tastes like raspberry juice'
            """))
            player.health = min(player.health + 20, player.maxhealth)
            print("You feel rejuvenated and your health is: %d" % player.health)
        elif 'health potion' not in player.items:
            print("You don't have any health potions in your bag.")

    elif action == 'use strength potion':
        if 'strength potion' in player.items:
            print(dedent("""
            You swallow the green liquid before you have time to think better of it.
            It doesn't take long before you start to feel stronger
            """))
            player.attack += 5
            print("Your new attack is now: %d" % player.attack)
        elif 'strength potion' not in player.items:
            print("You don't have any strength potions in your bag.")

    elif action == 'use small key':
        if 'small key' not in player.items:
            print("You don't have a small key in your bag.")
        elif not room.door:
            print("There is no door here to use the small key on.")
        elif room.door and not room.door_unlocked and 'small key' in player.items:
            print(dedent("""
            You use the small key you found earlier and insert it into the
            lock. You hear a click as you turn the key. The door is now unlocked.
            """))
            player.items.remove('small key')
            room.door_unlocked = True
        else:
            print("You have already used a key to unlock the door. No need to do it again.")

    elif action == 'use boss key':
        if 'boss key' not in player.items:
            print("You don't have a boss key in your bag.")
        elif not room.boss_door:
            print("There is no boss door here to use the boss key on.")
        elif room.door and not room.boss_door_unlocked and 'boss key' in player.items:
            print(dedent("""
            You use the boss key you found in the chest and insert it into the omnious lock.
            You have to use both of your hands to turn the key. When you have turned it a full
            90 degrees you hear a click. The door to the dungeon master is now unlocked.
            """))
            player.items.remove('boss key')
            room.boss_door_unlocked = True
        else:
            print("You have already used a key to unlock the door. No need to do it again.")

    elif action == 'fight' or action == 'attack':
        if room.monster:
            print("You decide that you want to attack the monster")
            if random.randint(0, MAX_AGILITY) > room.monster.agility:
                print("You manage to land your hit on the monster!")
                damage = random.randint(5, max(5, player.attack - math.floor(room.monster.defence / 2)))
                room.monster.health -= damage
                print("The hit does %d in damage" % damage)
                if room.monster.health <= 0:
                    room.monster = False
                    print("The monster in this room has been defeated.\n")
                    return player, action, room
                else:
                    print("The monster still has %d Health points left" % room.monster.health)
            else:
                print("Your attack misses and you are wide open.")

            action = None
            print("After your attack the monster recovers and launches an attack of its own.")
            if random.randint(0, MAX_AGILITY) > player.agility:
                print("The attack from the monster lands and you feel the damage.")
                damage = random.randint(5, max(5, room.monster.attack - math.floor(player.defence / 2)))
                player.health -= damage
                print("The hit does %d in damage" % damage)
                if player.health <= 0:
                    print(dedent("""
                    The attack from the monster is one wound too many. You feel the
                    strength failing you ask you fall to the ground and everything becomes dark.
                    """))
                    self.death()
                else:
                    print("You still has %d Health points left" % player.health)
            else:
                print("You dodge the monsters attack and get ready for the next round.")
        else:
            print("You can't do that here. There is no monster to attack")
            action = None

    elif action == 'run':
        print("You decide that it is better to turn tail and run back to the previous room")
        if random.randint(0, MAX_AGILITY - 20) > player.agility:
            print(dedent("""
            As you turn to run the monster lashes out with a wide swing that catches you in
            the back. You stumbled to the side, hurt and unable to escape.
            """))
            damage = random.randint(5, max(5, room.monster.attack - math.floor(player.defence / 2)))
            player.health -= damage
            action = None
            if player.health > 0:
                print("After taking the hit your health is: %d" % player.health)
            else:
                print(dedent("""
                The attack from the monster is one wound too many. You feel the strength failing you ask you fall to the ground and everything becomes dark.
                """))
                self.death()
        else:
            print(dedent("""
            As the monster attacks you skillfully avoid the deadly attack and get back the
            same way you came in.
            """))
            next_pos = player.prev_pos
            player.update_pos(next_pos[0], next_pos[1])

    elif action == 'avoid':
        print("You decide to try and avoid the next attack and slip out of the room.")
        if random.randint(0, MAX_AGILITY) > player.agility:
            print(dedent("""
            As you try to avoid the next attack, you slip and take the attack across your chest.
            Hurt you stumbled back to the corner.
            """))
            damage = random.randint(5, max(10, room.monster.attack - math.floor(player.defence / 2)))
            player.health -= damage
            action = None
            if player.health > 0:
                print("After taking the hit your health is: %d" % player.health)
            else:
                print(dedent("""
                The attack from the monster is one wound too many. You feel the strength
                failing you ask you fall to the ground and everything becomes dark.
                """))
                self.death()
        else:
            print("As the monster attacks you skillfully avoid the deadly attack and you are free to choose your exit.")
            room.monster_avoid = True

    elif action == 'rest':
        print(dedent("""
        You feel tired and figure that you need to recuperate some energy. Despite the risk of getting
        ambushed during th night you choose to take some quick shut-eye.
        """))
        player.health = min(player.health + 10, player.maxhealth)
        print("You feel rested and your health is: %d" % player.health)

    return player, action, room

def death(self):
    print(dedent(f"""
    The dungeon proved to be your master and your body is now forever entombed within its walls.
    You did your best but this is the end of '{player.name}'

    GAME OVER\n
    """))
    exit(1)
