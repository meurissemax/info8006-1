# Uniform Cost Search (UCS)
# Group: MEURISSE Maxime and VERMEYLEN Valentin

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        self.solution = []
        self.iterator = -1

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

        # If no solution has already been calculated.
        if self.iterator == -1:

            # Initialization of the fringe and the visited nodes.
            fringe = PriorityQueue()
            visited = set()

            # Pushing the initial state in the fringe.
            cost = len(self.solution)
            fringe.push((state, []), cost)

            while not fringe.isEmpty():
                # Pop of the next pacman state.
                current, self.solution = fringe.pop()[1]

                position = current.getPacmanPosition()
                food = current.getFood()

                # If the state was already visited, we go directly to the next.
                if (position, food) in visited:
                    continue

                # Else, we add it to the visited nodes.
                visited.add((position, food))

                # If all the dots are eaten, we stop: Pacman wins!
                if current.isWin():
                    break

                # Otherwise, we add the unvisited states to the fringe.
                for (child, action) in current.generatePacmanSuccessors():
                    position = child.getPacmanPosition()
                    food = child.getFood()

                    if (position, food) not in visited:
                        cost = len(self.solution)
                        fringe.push((child, self.solution + [action]), cost)

        # If a solution has been found, it is returned.
        self.iterator += 1

        return self.solution[self.iterator]
