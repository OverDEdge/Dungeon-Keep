"""Trap Room class"""

from room import *

class TrapRoom(Room):
    TRAPS = {'Roof falls down': 5, 'Trap door': 10, 'Arrows from wall': 15}
    P_TRAP = [0.7, 0.2, 0.1]
    def __init__(self, doors):
        super(TrapRoom, self).__init__(doors)
        # Generate a random trap
        self.trap = np.random.choice(list(self.TRAPS.keys()), 1, p = self.P_TRAP)
        # Print appropriate text

    def enter(self, player):
        if self.trap:
            if self.trap == 'Roof falls down':
                print(dedent("""
                    As soon as you step into the room debris start to rain down from above.
                    You dive for the corner but can't fully avoid the falling boulders.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            elif self.trap == 'Trap door':
                print(dedent("""
                    You take a few steps into the seemingly empty room. But on your third
                    step the ground opens up beneath you revealing a spiked floor.
                    Thanks to luck and the decrepit conditions of the spikes you are not
                    fully impaled, but you still take some damage.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            elif self.trap == 'Arrows from wall':
                print(dedent("""
                    As you survey the room you feel one of the tiles dip slightly under
                    your foot. You know this doesn't bode well and as soon as that
                    thought passes through your head, arrows start shooting out of the
                    nearby walls. You tuck and roll to escape the flying missiles but
                    a few still manage to find its mark.
                    """))
                print("You loose %d health" % self.TRAPS[self.trap[0]])
            else:
                print("Trap type isn't defined. Something has gone wrong. Exiting game")
                exit(1)
            player.health -= self.TRAPS[self.trap[0]]
        else:
            pass

        # Get previous direction of player
        self.came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room description
        super(TrapRoom, self).describe_room(self.came_from)

        # If trap is gone continue as standard room
        return super(TrapRoom, self).enter(player)

        #self.describe_room()
        # Get previous direction of player
        #came_from = self.get_prev_dir(player.position, player.prev_pos)
        # Show room descrition
        #self.describe_room(came_from)
