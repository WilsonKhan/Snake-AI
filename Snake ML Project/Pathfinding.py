import numpy as np
import heapq
from game_functions import GameState

class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0 # Distance between the current node and the START node
        self.h = 0 # Heuristic: Distance from current node to END node
        self.f = 0 # f is the total cost of the node, g + h.

def createStateArray(game_state):
    # Access attributes using the provided game_state instance
    State_Array = np.zeros((game_state.num_tiles_x, game_state.num_tiles_y))

    State_Array[game_state.current_apple_x][game_state.current_apple_y] = 2 # Render the apple as a 2

    # Render the Snake as a series of 1's
    for i in range(game_state.num_tiles_x):
        for j in range(game_state.num_tiles_y):
            if [i, j] in game_state.positions:
                State_Array[i][j] = 1

    print(State_Array)

def createStartEndNodes(head, apple_x, apple_y):
    start_node = Node(position = head)
    end_node = Node(position = [apple_x, apple_y])

def astar(start, end):
    open_set = [] # Nodes to be evaluated
    closed_set = set() # Already evaluated nodes

def heuristic(current_node, end_node):
    heuristic = (end_node.position[0] - current_node.position[0])**2 * (end_node.position[1] - current_node.position[1])**2
    return heuristic

def get_neighbours():
    pass