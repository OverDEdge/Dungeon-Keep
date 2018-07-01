"""Monster Room class"""

from room import *

class MonsterRoom(Room):
    def __init__(self, doors):
        super(MonsterRoom, self).__init__(doors)
        # Generate a random monster for this room
        self.monster = Monster(random.choice(list(MONSTER_STATS.keys())))

    # Function that activates when Player enters room
    def enter(self, player):
        self.monster_avoid = False

        # Check if monster has been defeated or not
        if self.monster:
            # Get previous direction of player
            self.came_from = self.get_prev_dir(player.position, player.prev_pos)
            # Show room description
            super(MonsterRoom, self).describe_room(self.came_from)
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
                    You quietly enter the room and take a quick look back since you don't want
                    anyone sneaking up on you from behind. As you turn back around you
                    suddenly hear a high pitched screech coming from a dark corner. Out
                    strolls a small evil Looking creature with sharp teeth. Great, you
                    just stepped into the territory of a Dark Elf.
                    """))
            else:
                print("Monster type not defined. Something has gone wrong. Exiting game.")
                exit(1)

            # Save position to check it run successful.
            temp_pos = player.position
            # Start fight sequence
            player = super(MonsterRoom, self).enter(player, MR_ACTIONS_PRE, MR_ACTION_PRE_MESSAGE, ['fight', 'attack', 'run', 'avoid'])

            if self.monster_avoid:
                # If player has managed to avoid the monster he can choose the exit
                return super(MonsterRoom, self).enter(player, MR_ACTIONS_AVOID, MR_ACTION_AVOID_MESSAGE)
            elif temp_pos != player.position:
                # If player has sucessfully run away from monster
                player.prev_pos = temp_pos
                return player
            else:
                # Monster has been defeated and can continue exploring the room
                print("After defeating the monster the room is clear to explore")
                return super(MonsterRoom, self).enter(player)
        else:
            pass

        print("The monster in this room has been defeated.\n")

        # SInce the monster is gone continue as standard room

        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(MonsterRoom, self).describe_room(self.came_from)
        return super(MonsterRoom, self).enter(player)
