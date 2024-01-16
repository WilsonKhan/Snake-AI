import numpy as np
import heapq
from game_functions import GameState, grid_offset

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = tuple(position)
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

def createStateArray(game_state, grid_size):
    # Access attributes using the provided game_state instance
    State_Array = np.zeros((game_state.num_tiles_x, game_state.num_tiles_y))

    # Convert the apple from pixel position to grid position and render it as a 2 in the state array.
    State_Array[(game_state.current_apple_y-grid_offset)//grid_size][(game_state.current_apple_x-grid_offset)//grid_size] = 2

    # Render the Snake as a series of 1's
    for i in range(game_state.num_tiles_x):
        for j in range(game_state.num_tiles_y):
            if [i, j] in game_state.positions:

                # Flipped i and j coords because as far as I can tell the screen generation in pygame works differently to normal arrays.
                State_Array[j][i] = 1 

    print(State_Array)

def createStartEndNodes(head, apple_x, apple_y, grid_size):
    grid_apple_x = (apple_x - grid_offset) // grid_size
    grid_apple_y = (apple_y - grid_offset) // grid_size
    start_node = Node(position=[head[0], head[1]])
    end_node = Node(position=[grid_apple_x, grid_apple_y])
    return start_node, end_node

def astar(start, end, width, height, grid_size, snake_body):
    open_set = []
    open_set_positions = set()
    closed_set = set()

    heapq.heappush(open_set, (start.f, start))
    open_set_positions.add(start.position)

    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_positions.remove(current.position)
        #print(f"Processing node at {current.position}, f: {current.f}, g: {current.g}, h: {current.h}")
        if current == end:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_set.add(current)

        for neighbour in get_neighbours(current, width, height, grid_size, snake_body):
            if neighbour in closed_set:
                continue

            tentative_g = current.g + 1

            if neighbour.position not in open_set_positions or tentative_g < neighbour.g:
                neighbour.g = tentative_g
                neighbour.h = heuristic(neighbour, end)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.parent = current

                if neighbour.position not in open_set_positions:
                    heapq.heappush(open_set, (neighbour.f, neighbour))
                    open_set_positions.add(neighbour.position)

    return None


def heuristic(current_node, end_node):
    return abs(end_node.position[0] - current_node.position[0]) + abs(end_node.position[1] - current_node.position[1])

def get_neighbours(node, width, height, grid_size, snake_body):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Convert snake body positions to tuples for consistent comparison
    snake_body_tuples = set(tuple(pos) for pos in snake_body)

    for direction in directions:
        neighbor_x = node.position[0] + direction[0]
        neighbor_y = node.position[1] + direction[1]

        tuple_for_comparison = (neighbor_x, neighbor_y)

        if ((0 <= neighbor_x < (width) // grid_size) and
            (0 <= neighbor_y < (height) // grid_size) and
            tuple_for_comparison not in snake_body_tuples):
                neighbors.append(Node(position=(neighbor_x, neighbor_y)))

    return neighbors

def findDirection(astar_path, head):
    if not astar_path:
        return [1, 0]  # Emergency default, or you could return None to indicate no path.

    next_position = astar_path[0] if len(astar_path) == 1 else astar_path[1]

    # Calculate direction based on the next position
    if next_position[0] == head[0] + 1 and next_position[1] == head[1]:
        return [1, 0]
    elif next_position[0] == head[0] - 1 and next_position[1] == head[1]:
        return [-1, 0]
    elif next_position[0] == head[0] and next_position[1] == head[1] + 1:
        return [0, 1]
    elif next_position[0] == head[0] and next_position[1] == head[1] - 1:
        return [0, -1]

    return [-1, 0]# Emergency default, or handle this case as needed


