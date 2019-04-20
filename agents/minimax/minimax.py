# Implementation of the Minimax algorithm.
#
# Group:
#   - MEURISSE Maxime (20161278)
#   - VERMEYLEN Valentin (20162864)
#
# Project for the course INFO8006
# Academic year 2018-2019

from pacman_module.game import Agent
from pacman_module.pacman import Directions

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

    def terminal(self, state, visited):
        """
        Check if the calculations should stop or not.

        Arguments:
        ----------
        - `state`: the current game state.
        - `visited`: the list of substates already visited.

        Return:
        -------
        - A boolean value.
        """
        if state.isWin() or state.isLose():
            return True

        if self.is_cycle(state, visited):
            return True

        return False

    def utility(self, state, player):
        """
        Given an agent game state, returns a numerical value that
        estimates this state.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.

        Return:
        -------
        - A numerical value.
        """
        if state.isWin() or state.isLose():
            return state.getScore()

        # In case of cycle.
        if player == PACMAN:
            return INFINITY
        else:
            return -INFINITY

    def max_player(self, state, player, visited):
        """
        Returns the numerical value associated with the state chosen
        by the MAX player.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.

        Return:
        -------
        - A numerical value.
        """
        max_v = -INFINITY

        successors = state.generatePacmanSuccessors()

        for child, action in successors:
            next_p = self.player(state, player)
            next_v = self.deepcopy_list(visited)

            value = self.minimax(child, next_p, next_v)
            max_v = max(max_v, value)

        return max_v

    def min_player(self, state, player, visited):
        """
        Returns the numerical value associated with the state chosen
        by the MIN player.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.

        Return:
        -------
        - A numerical value.
        """
        min_v = INFINITY

        successors = state.generateGhostSuccessors(player)

        for child, action in successors:
            next_p = self.player(state, player)
            next_v = self.deepcopy_list(visited)

            value = self.minimax(child, next_p, next_v)
            min_v = min(min_v, value)

        return min_v

    def minimax(self, state, player, visited):
        """
        Returns the numerical value associated with the next game state.

        Arguments:
        ----------
        - `state`: the current game state.
        - `player`: the numerical value of the current player.
        - `visited`: the list of substates already visited.

        Return:
        -------
        - A numerical value.
        """
        if self.terminal(state, visited[player]):
            return self.utility(state, player)

        if player == PACMAN:
            return self.max_player(state, player, visited)
        else:
            return self.min_player(state, player, visited)

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

        # We initialize the visited list. This is a list
        # containing a list by agent.
        num = state.getNumAgents()
        visited = [None] * num

        for i in range(num):
            visited[i] = []

        for child, action in state.generatePacmanSuccessors():
            next_p = self.player(state, PACMAN)

            value = self.minimax(child, next_p, visited)

            if value >= max_v:
                max_v, next_a = value, action

        return next_a
