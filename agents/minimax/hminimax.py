# Implementation of the H-Minimax (with alpha-beta pruning) algorithm.
#
# Group:
#   - MEURISSE Maxime (20161278)
#   - VERMEYLEN Valentin (20162864)
#
# Project for the course INFO8006
# Academic year 2018-2019

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance

PACMAN = 0
INFINITY = float('inf')


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        # The depth in the tree at which the calculations are limited.
        self.max_depth = 10

    def deepcopy_list(self, list):
        """
        Given a list, returns a deep copy of this list.

        Arguments:
        ----------
        - `list`: the list to copy.

        Return:
        -------
        - The copy of the list.
        """
        copy = list.copy()

        for i in range(len(list)):
            copy[i] = list[i].copy()

        return copy

    def player(self, state, current):
        """
        Given an agent game state and the current player, returns the
        numerical value that determines the next player.

        Arguments:
        ----------
        - `state`: the current game state.
        - `current`: the numerical value of the current player.

        Return:
        -------
        - The numerical value that determines the next player.
        """
        return (current + 1) % state.getNumAgents()

    def is_cycle(self, state, visited):
        """
        Checks if a substate has already been visited in a branch
        development.

        Arguments:
        ----------
        - `state`: the current game state.
        - `visited`: the list of substates already visited.

        Return:
        -------
        - A boolean value.
        """
        substate = (state.getPacmanPosition(),
                    state.getGhostPositions(),
                    state.getFood())

        if substate in visited:
            return True
        else:
            visited.append(substate)

            return False

    def min_distance_ghost(self, state):
        """
        Calculates the minimum distance between Pacman and the
        nearest ghost.

        Arguments:
        ----------
        - `state`: the current game state.

        Return:
        -------
        - The minimum distance between Pacman and the nearest ghost.
        """
        distance_min = INFINITY
        pacman_pos = state.getPacmanPosition()

        for ghost_pos in state.getGhostPositions():
            distance = manhattanDistance(pacman_pos, ghost_pos)

            if distance < distance_min:
                distance_min = distance

        return distance_min

    def min_distance_food(self, state):
        """
        Calculates the minimum distance between Pacman and the
        nearest dot.

        Arguments:
        ----------
        - `state`: the current game state.

        Return:
        -------
        - The minimum distance between Pacman and the nearest dot.
        """
        distance_min = INFINITY
        pacman_pos = state.getPacmanPosition()
        food = state.getFood()
        position = [-1, -1]

        for x in food:
            position[0] += 1
            position[1] = -1

            for y in x:
                position[1] += 1

                if y:
                    distance = manhattanDistance(pacman_pos, position)

                    if distance < distance_min:
                        distance_min = distance

        return distance_min

    def cutoff(self, state, visited, depth):
        """
        Check if the calculations should stop or not.

        Arguments:
        ----------
        - `state`: the current game state.
        - `visited`: the list of substates already visited.
        - `depth`: the current depth in the tree.

        Return:
        -------
        - A boolean value.
        """
        if state.isWin() or state.isLose():
            return True

        if self.is_cycle(state, visited):
            return True

        if depth >= self.max_depth:
            return True

        return False

    def evaluation(self, state):
        """
        Given an agent game state, returns a numerical value that
        estimates this state.

        This evaluation fonction is partially adapted from:
        https://gist.github.com/dcalacci/695374

        Arguments:
        ----------
        - `state`: the current game state.

        Return:
        -------
        - A numerical value.
        """
        score = state.getScore()

        if state.isWin() or state.isLose():
            return score

        food = state.getFood()
        pacman_pos = state.getPacmanPosition()
        ghost_min = self.min_distance_ghost(state)
        food_min = self.min_distance_food(state)
        food_number = 0

        for list in food:
            food_number += sum(list)

        value = score - 1.5 * food_min - (2 / (ghost_min)) - 4 * food_number

        return value

    def max_player(self, state, player, visited, alpha, beta, depth):
        """
        Returns the numerical value associated with the state chosen
        by the MAX player.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.
        - `alpha`: the alpha value in order to make the alpha-beta pruning.
        - `beta`: the beta value in order to make the alpha-beta pruning.
        - `depth`: the current depth in the tree.

        Return:
        -------
        - A numerical value.
        """
        max_v = -INFINITY

        successors = state.generatePacmanSuccessors()

        for child, action in successors:
            next_p = self.player(state, player)
            next_v = self.deepcopy_list(visited)
            next_d = depth + 1

            value = self.minimax(child, next_p, next_v, alpha, beta, next_d)
            max_v = max(max_v, value)

            if max_v >= beta:
                return max_v

            alpha = max(alpha, max_v)

        return max_v

    def min_player(self, state, player, visited, alpha, beta, depth):
        """
        Returns the numerical value associated with the state chosen
        by the MIN player.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.
        - `alpha`: the alpha value in order to make the alpha-beta pruning.
        - `beta`: the beta value in order to make the alpha-beta pruning.
        - `depth`: the current depth in the tree.

        Return:
        -------
        - A numerical value.
        """
        min_v = INFINITY

        successors = state.generateGhostSuccessors(player)

        for child, action in successors:
            next_p = self.player(state, player)
            next_v = self.deepcopy_list(visited)
            next_d = depth + 1

            value = self.minimax(child, next_p, next_v, alpha, beta, next_d)
            min_v = min(min_v, value)

            if min_v <= alpha:
                return min_v

            beta = min(beta, min_v)

        return min_v

    def minimax(self, state, player, visited, alpha, beta, depth):
        """
        Returns the numerical value associated with the next game state.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.
        - `alpha`: the alpha value in order to make the alpha-beta pruning.
        - `beta`: the beta value in order to make the alpha-beta pruning.
        - `depth`: the current depth in the tree.

        Return:
        -------
        - A numerical value.
        """
        if self.cutoff(state, visited[player], depth):
            return self.evaluation(state)

        if player == PACMAN:
            return self.max_player(state, player, visited, alpha, beta, depth)
        else:
            return self.min_player(state, player, visited, alpha, beta, depth)

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        max_v = -INFINITY
        next_a = Directions.STOP
        alpha = -INFINITY
        beta = INFINITY
        successors = state.generatePacmanSuccessors()
        values = list()

        # We initialize the visited list. This is a list
        # containing a list by agent.
        num = state.getNumAgents()
        visited = [None] * num

        for i in range(num):
            visited[i] = []

        substate = (state.getPacmanPosition(),
                    state.getGhostPositions(),
                    state.getFood())

        visited[0].append(substate)

        for child, action in successors:
            next_p = self.player(state, PACMAN)

            value = self.minimax(child, next_p, visited, alpha, beta, 0)
            values.append(value)

            if value >= max_v:
                max_v, next_a = value, action

        # If all your moves have the same value, choose the one that
        # is immediately optimal. But if you are dying no matter what,
        # do it as soon as possible (max_v < -300 in that case).
        if values.count(max_v) > 1 and max_v > -300:
            value = -INFINITY

            for child, action in successors:
                new = self.evaluation(child)

                if new > value:
                    value, next_a = new, action

        return next_a
