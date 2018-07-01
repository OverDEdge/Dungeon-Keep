"""Secret Room class"""

from room import *
from textwrap import dedent

class SecretRoom(Room):
    SECRET_ITEMS = ['Mjolnir', 'Elder Wand', 'Cloak of Mobility', 'Bow of Tell']
    #SECRET_ITEMS = ['Bow of Tell']
    P_ITEMS = [0.25, 0.25, 0.25, 0.25]
    #P_ITEMS = [1]
    RIDDLES = {
    "A box without hinges, keyhole or lid,\nbut still a golden treasure inside is hid.\nWhat am I?": ['egg', 'an egg', 'the egg', 'eggs', 'a egg'],
    "The answer to life, the universe and everything": ['42', 'forty two', 'forty-two'],
    "On my way to St. Mary's I met a woman with seven children.\nEvery child had seven cats and every cat had seven kitten.\n How many where going to St. Mary's?": ['one', '1', 'me'],
    "There is a crime for which you can only be arrested while attempting it.\nBut not after you have committed it.\nWhat is it?": ['suicide', 'suicide attempt', 'taking ones life', 'killing yourself'],
    "What travels around the world,\nbut stays in the same corner?": ['stamp', 'a stamp', 'the stamp'],
    "If I have it, I do not share it.\nIf I share it, I do not have it.\nWhat is it?": ['secret', 'a secret', 'the secret']
    }

    def __init__(self, doors):
        super(SecretRoom, self).__init__(doors)
        self.item = np.random.choice(self.SECRET_ITEMS, 1, p = self.P_ITEMS)[0].lower()
        self.riddle = False

    def enter(self, player):
        # Do special stuff for SecretRoom in case of search

        if not self.riddle:

            print(dedent("""
            As you walk down the dark corridor you notice a shape up ahead. You warely
            approach and as you get closer you notice that it looks like the statue of
            a sphynx. You have heard of these creatures:
            They pose riddles to travelers and if they get it right great riches await,
            but if they get it wrong... Well since no one have ever come back and told
            of getting it wrong the riddles are either very easy or the consequences very
            dire.
            """))

            action = None

            while action != '1' and action != '2':
                action = input("Do you:\n1. Approach\n2. Turn back\n-> ")
                if action != '1' and action != '2':
                    print("Please answer with '1' or '2'")

            if action == '1':
                print("You have chosen to approach the sphynx and accept the challenge it poses.")
                print(dedent("""
                As you approach the sphynx lifts opens it's eyes and says.
                'Before I pose my question I give one advise. All questions have short anwers,
                please just use one or two words in your answer to make a fair ruling. Now listen carefully!'
                """))
                print("RIDDLE:")
                riddle = random.choice(list(self.RIDDLES.keys()))
                print(riddle)
                answer = input("-> ").lower()
                if answer in self.RIDDLES[riddle]:
                    print(f"You, '{player.name}', have answered...\nCorrectly!\nYou may proceed to the next room. Well done dear warrior!")
                    self.riddle = True
                    print("There must be something special up ahead since it was being guarded by this sphynx.\n")
                else:
                    print(f"You, '{player.name}', have answered...\nPoorly!")
                    print(dedent("""
                    The sphynx suddenly transforms to a living beast and before you have time to react
                    it swallows you whole. Not the way you wanted to go but that is the risk you take
                    when dealing with a sphynx.

                    GAME OVER!!!
                    """))
                    exit(1)
            else:
                print("You choose to turn back. Probably a wise choice, who knows what kind of questions that creature would ask!\n")
                old_pos = player.position
                player.position = player.prev_pos
                player.prev_pos = old_pos
                return player

        else:
            # Riddle has been solved so jsut continue into room
            pass

        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(SecretRoom, self).describe_room(self.came_from)

        # If secret is found update stats accordingly then continue as standard room
        return super(SecretRoom, self).enter(player)
