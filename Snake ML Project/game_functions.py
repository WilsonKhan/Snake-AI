import pygame
import random
import colorsys

# Offsets the icons from the grid for visibility
grid_offset = 3
apple_offset = 4

class GameState:
    def __init__(self, num_tiles_x, num_tiles_y, grid_size):
        self.num_tiles_x = num_tiles_x
        self.num_tiles_y = num_tiles_y
        self.grid_size = grid_size

        self.width = self.num_tiles_x * self.grid_size
        self.height = self.num_tiles_y * self.grid_size

        self.screen = pygame.display.set_mode((self.width, self.height))

        #Initialise a random apple position when the first instance of the class is created
        self.current_apple_x = self.grid_size * random.randint(0, self.num_tiles_x - 1) + grid_offset 
        self.current_apple_y = self.grid_size * random.randint(0, self.num_tiles_y - 1) + grid_offset

        self.positions = [[2, 2]] # Sets the initial position

    def generate_rainbow_colors(self, num_colors):
        # Generate a list of rainbow colors
        return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in [colorsys.hsv_to_rgb(i / num_colors, 1.0, 1.0) for i in range(num_colors)]]

    def Draw_Apple(self, Apple_Eaten):
        # If apple isn't eaten, draw it at the same coordinates
        if not Apple_Eaten:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.current_apple_x, self.current_apple_y, self.grid_size-apple_offset, self.grid_size-apple_offset))
        else:
            apple_placed = False
            while not apple_placed:
                new_apple_x = random.randint(0, self.num_tiles_x - 1)
                new_apple_y = random.randint(0, self.num_tiles_y - 1)
                apple_pos = [new_apple_x, new_apple_y]
                apple_pixel_pos = [new_apple_x * self.grid_size + grid_offset, new_apple_y * self.grid_size + grid_offset]
                
                # Check if the new apple position overlaps with the snake's body
                if apple_pos not in self.positions:
                    pygame.draw.rect(self.screen, (255, 0, 0), (apple_pixel_pos[0], apple_pixel_pos[1], self.grid_size - apple_offset, self.grid_size - apple_offset))
                    self.current_apple_x, self.current_apple_y = apple_pixel_pos
                    apple_placed = True

    def generate_new_apple(self):
        apple_placed = False
        while not apple_placed:
            new_apple_x = random.randint(0, self.num_tiles_x - 1)
            new_apple_y = random.randint(0, self.num_tiles_y - 1)
            apple_pos = [new_apple_x, new_apple_y]
            apple_pixel_pos = [new_apple_x * self.grid_size + grid_offset, new_apple_y * self.grid_size + grid_offset]
                
            # Check if the new apple position overlaps with the snake's body
            if apple_pos not in self.positions:
                self.current_apple_x, self.current_apple_y = apple_pixel_pos
                apple_placed = True


    # Draws lines vertically and horizontally from the borders of the screen
    def Draw_Grid(self):
        for i in range(self.num_tiles_x):
            start_pos_y = (i * self.grid_size, 0)
            end_pos_y = (i * self.grid_size, self.height)
            start_pos_x = (0, i * self.grid_size)
            end_pos_x = (self.width, i * self.grid_size)
            pygame.draw.line(self.screen, (255, 255, 255), start_pos_y, end_pos_y, 2) # Draw lines with thickness 2 pixels
            pygame.draw.line(self.screen, (255, 255, 255), start_pos_x, end_pos_x, 2)

    # If an apple has been eaten, the tail of the snake that is supposed to be deleted as the snake moves is not deleted
    def append_positions(self, Apple_Eaten, direction):
        new_head = [self.positions[0][0] + direction[0], self.positions[0][1] + direction[1]]
        self.positions.insert(0, new_head)
        if not Apple_Eaten:
            self.positions.pop()

    def print_snake(self, score):
        num_colors = len(self.positions)
        rainbow_colors = self.generate_rainbow_colors(num_colors)

        for i in range(score + 1):
            color_index = i % num_colors
            pygame.draw.rect(self.screen, rainbow_colors[color_index], (self.positions[i][0] * self.grid_size + grid_offset, self.positions[i][1] * self.grid_size + grid_offset, self.grid_size - apple_offset, self.grid_size - apple_offset))

    def check_collision(self):
        # Check if the head collides with any other part of the snake
        head = self.positions[0]
        if head in self.positions[1:]:
            return True
        if (head[0] * self.grid_size >= self.width) or (head[0] * self.grid_size < 0) or (head[1] * self.grid_size >= self.height) or (head[1] * self.grid_size < 0):
            return True
        return False
    
    def draw_astar_path(self, path, grid_size):
        if path:
            for node in path[1:-1]:
                x, y = node
                pygame.draw.rect(self.screen, (128, 128, 128), (x * grid_size + grid_offset, y * grid_size + grid_offset, grid_size - grid_offset, grid_size - grid_offset))