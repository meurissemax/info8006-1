# Bayes filter for Pacman
# Authors: Maxime Meurisse & Valentin Vermeylen

from pacman_module import util
from pacman_module.game import Agent
from pacman_module.pacman import Directions, GhostRules
import numpy as np
import copy as cp


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'updateAndFetBeliefStates' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None
        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None
        # Uniform distribution size parameter 'w'
        # for sensor noise (see instructions)
        self.w = self.args.w
        # Probability for 'leftturn' ghost to take 'EAST' action
        # when 'EAST' is legal (see instructions)
        self.p = self.args.p

    def transition(self, cur, prev, width, height):
        """
        Given a previous position on the map and known positions
        of the walls, returns the probability of going from
        position prev to current position.

        Arguments:
        ----------
        - `cur`: the current position being evaluated
        - `prev`: a previous possible position
        - `width`: the width of the maze
        - `height`: the height of the maze

        Return:
        -------
        - The probability of being in position current
          from the position prev.
        """
        p = self.p
        walls = self.walls

        # Number of legal actions of the previous position
        number = 0

        # Could we go east while in prev ?
        east = False

        # The ghost cannot stop. It is not a legal action
        if cur == prev:
            return 0

        # If we are in a wall or trying to get out of a wall,
        # impossible. Probability is 0.
        if walls[cur[0]][cur[1]] or walls[prev[0]][prev[1]]:
            return 0

        # The ghost cannot move diagonally.
        if (prev[0] + 1 == cur[0] and prev[1] + 1 == cur[1]) \
                or (prev[0] + 1 == cur[0] and prev[1] - 1 == cur[1]) \
                or (prev[0] - 1 == cur[0] and prev[1] + 1 == cur[1]) \
                or (prev[0] - 1 == cur[0] and prev[1] - 1 == cur[1]):
            return 0

        # How many legal actions could the ghost take in the previous
        # position ?
        if prev[0] + 1 < width and not walls[prev[0] + 1][prev[1]]:
            number += 1

        if prev[0] - 1 >= 0 and not walls[prev[0] - 1][prev[1]]:
            number += 1

        if prev[1] + 1 < height and not walls[prev[0]][prev[1] + 1]:
            number += 1

        if prev[1] - 1 >= 0 and not walls[prev[0]][prev[1] - 1]:
            number += 1

        if number == 0:
            return 0

        # Was east a legal move ?
        if prev[0] in range(0, width - 1) and not walls[prev[0] + 1][prev[1]]:
            east = True

        # Probability of going in a direction if east is possible
        prob = (1 - p) / number

        if cur[0] == (prev[0] + 1):
            return p + prob
        elif east:
            return prob
        else:
            return 1 / number

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of (noised) ghost positions at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t} about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates
        # XXX: Your code here

        beliefs = cp.deepcopy(beliefStates)
        w = self.w
        (ghosts, width, height) = beliefs.shape

        # Map will hold the ranges possible.
        map = list()
        map.extend((range(width), range(height)))

        # We iterate for all ghosts
        for ghost in range(ghosts):
            (x_g, y_g) = evidences[ghost]

            # Bounds in which the ghost could be thanks to sensor model
            bounds = list()

            limits = list()

            # We define the bounds of the W x W zone
            bounds.extend((x_g - w, x_g + w, y_g - w, y_g + w))

            # x where the ghost could be
            limits.append(range(bounds[0], bounds[1] + 1))

            # y where the ghost could be
            limits.append(range(bounds[2], bounds[3] + 1))

            # Normalization term
            alpha = 0

            # We iterate for all positions in the map
            for x in map[0]:
                for y in map[1]:
                    # If the position is not in the W x W zone, P = 0
                    if x not in limits[0] or y not in limits[1]:
                        beliefs[ghost][x][y] = 0
                    # Else the position is in the W x W zone
                    else:
                        # We get the sum of the products of the
                        # transition model by the beliefs
                        sum = 0

                        for i in range(x - 1, x + 2):
                            for j in range(y - 1, y + 2):
                                if i in map[0] and j in map[1]:
                                    terms = list()

                                    terms.append(self.transition((x, y),
                                                                 (i, j),
                                                                 width,
                                                                 height))
                                    terms.append(self.beliefGhostStates[ghost]
                                                                       [i]
                                                                       [j])

                                    sum += np.prod(terms)

                        # Sonar sensor model, no wall considered
                        beliefs[ghost][x][y] = 1 / ((2 * w + 1) ** 2)

                        # Multiplied by the sum of the products
                        # of the transition model by the beliefs
                        beliefs[ghost][x][y] *= sum

                    alpha += beliefs[ghost][x][y]

            # Normalization
            for x in map[0]:
                for y in map[1]:
                    beliefs[ghost][x][y] /= alpha

        beliefStates = cp.deepcopy(beliefs)

        # XXX: End of your code
        self.beliefGhostStates = beliefStates
        return beliefStates

    def _computeNoisyPositions(self, state):
        """
            Compute a noisy position from true ghosts positions.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        w = self.args.w
        w2 = 2*w+1
        div = float(w2 * w2)
        new_positions = []
        for p in positions:
            (x, y) = p
            dist = util.Counter()
            for i in range(x - w, x + w + 1):
                for j in range(y - w, y + w + 1):
                    dist[(i, j)] = 1.0 / div
            dist.normalize()
            new_positions.append(util.chooseFromDistribution(dist))
        return new_positions

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """

        # XXX : You shouldn't care on what is going on below.
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()
        return self.updateAndGetBeliefStates(
            self._computeNoisyPositions(state))
