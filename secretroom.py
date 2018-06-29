"""Secret Room class"""

from room import *

class SecretRoom(Room):
    SECRET_ITEMS = ['Mjolnir', 'Elder Wand', 'Cloak of Mobility']
    P_ITEMS = [0.3, 0.3, 0.4]
    def __init__(self, doors):
        super(SecretRoom, self).__init__(doors)
        self.items = np.random.choice(SECRET_ITEMS, 1, p = self.P_ITEMS)

    def enter(self, player):
        # Do special stuff for SecretRoom in case of search

        # If secret is found then continue as standard room
        return super(SecretRoom, self).enter(player)
