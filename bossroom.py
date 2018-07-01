"""Boss Room class"""

from room import *
from sys import exit

class BossRoom(Room):

    def __init__(self, doors):
        super(BossRoom, self).__init__(doors)
        self.boss_door = True
        self.monster = Dragon(random.choice(list(BOSS_STATS.keys())))

    def enter(self, player):
        # Do special stuff for BossRoom
        print(dedent("""
        As you stumble along the corridor you are faced with a massive door.
        It is adorned with a massive beast head and you have no doubt that the
        master of this dungeon is hiding behind that door.
        """))
        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Save current position to check after asking for action
        old_pos = player.position
        player =  super(BossRoom, self).enter(player, BR_ACTIONS_PRE, BR_ACTION_PRE_MESSAGE,
                    ['use boss key', 'open door', 'go back'])

        # Check if monster has been defeated or not
        if self.monster:
            print(dedent("""
            You follow the dark passage until you notice the walls are spreading and you enter
            a massive chamber. You can't even see the roof or the other side of the room.

            As you quietly move forward you hear a massive roar coming from the dark reaches of
            the room. You can feel the ground shaking as, whatever it is, moves toward you. You
            get ready to fight.
            """))

            print("Out into the light steps a large '%s' and fixes on you with a hateful stare" % self.monster.type)
            # Save position to check if player choose to run and it was successful.
            temp_pos = player.position
            # Start fight sequence
            player = super(BossRoom, self).enter(player, BR_ACTIONS_POST, BR_ACTION_POST_MESSAGE, ['fight', 'attack', 'run', 'avoid'])
            if self.monster_avoid:
                # If player has managed to avoid the monster he can choose the exit
                return super(BossRoom, self).enter(player, BR_ACTIONS_AVOID, BR_ACTION_AVOID_MESSAGE)
            elif temp_pos != player.position:
                # If player has sucessfully run away from monster
                player.prev_pos = temp_pos
                return player
            else:
                pass
                # The boss has been defeated.
        else:
            pass

        print(dedent("""
        You have defeated the boss of this dungeon and can now call yourself the true 'Dungeon Master'
        As you move around the body of the massive monster you notice a shine coming from a small
        alcove. Inside you find the largest diamond you have ever seen, probably worth more than you
        could ever spend in a lifetime. A well deserved price for such a skilled and brave warrior.

        You safely exit the dungeon to look towards new horizaons and adventures.
        """))
        print("Congratulations %s! THE END!" % player.name)
        exit(1)
