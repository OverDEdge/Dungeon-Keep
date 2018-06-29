"""Monster Room class"""

from room import *

class MonsterRoom(Room):
    def __init__(self, doors):
        super(MonsterRoom, self).__init__(doors)
        # Generate a random monster for this room
        self.monster = Monster(random.choice(list(MONSTER_STATS.keys())))

    # Function that activates when Player enters room
    def enter(self, player):

        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(MonsterRoom, self).describe_room(self.came_from)
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
                    You quietly enter the room and quickly looking back since don't want
                    anyone sneaking up on you from behind. As you turn back around you
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
        return super(MonsterRoom, self).enter(player)
        # Get previous direction of player
        #came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room descrition
        #self.describe_room(came_from)

        # Ask for player action
        # Keep going until action to leave room is detected
