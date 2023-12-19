import pygame
import sys
import random
import colorsys

def generate_rainbow_colors(num_colors):
    # Generate a list of rainbow colors
    return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in [colorsys.hsv_to_rgb(i / num_colors, 1.0, 1.0) for i in range(num_colors)]]

def Draw_Apple(Apple_Eaten):
    global current_apple_x, current_apple_y
    # If apple isn't eaten, draw it at the same coordinates
    if not Apple_Eaten:
        pygame.draw.rect(screen, (255, 0, 0), (current_apple_x, current_apple_y, grid_size-4, grid_size-4))
    else:
        apple_placed = False
        while not apple_placed:
            new_apple_x = random.randint(0, num_tiles_x - 1)
            new_apple_y = random.randint(0, num_tiles_y - 1)
            apple_pos = [new_apple_x, new_apple_y]
            apple_pixel_pos = [new_apple_x * grid_size + 3, new_apple_y * grid_size + 3]
            
            # Check if the new apple position overlaps with the snake's body
            if apple_pos not in positions:
                pygame.draw.rect(screen, (255, 0, 0), (apple_pixel_pos[0], apple_pixel_pos[1], grid_size-4, grid_size-4))
                current_apple_x, current_apple_y = apple_pixel_pos
                apple_placed = True

# Draws lines vertically and horizontally from the borders of the screen
def Draw_Grid():
    for i in range(num_tiles_x):
        start_pos_y = (i * grid_size, 0)
        end_pos_y = (i * grid_size, height)
        start_pos_x = (0, i * grid_size)
        end_pos_x = (width, i * grid_size)
        pygame.draw.line(screen, (255, 255, 255), start_pos_y, end_pos_y, 2)
        pygame.draw.line(screen, (255, 255, 255), start_pos_x, end_pos_x, 2)

# If an apple has been eaten, the tail of the snake that is supposed to be deleted as the snake moves is not deleted
def append_positions(positions, Apple_Eaten, direction):
    new_head = [positions[0][0] + direction[0], positions[0][1] + direction[1]]
    positions.insert(0, new_head)
    if not Apple_Eaten:
        positions.pop()


def print_snake(positions, score):
    num_colors = len(positions)
    rainbow_colors = generate_rainbow_colors(num_colors)

    for i in range(score + 1):
        color_index = i % num_colors
        pygame.draw.rect(screen, rainbow_colors[color_index], (positions[i][0] * grid_size + 3, positions[i][1] * grid_size + 3, grid_size-4, grid_size-4))

def check_collision(positions):
    # Check if the head collides with any other part of the snake
    head = positions[0]
    if head in positions[1:]:
        return True
    if (head[0] * grid_size >= width) or (head[0] * grid_size < 0) or (head[1] * grid_size >= height) or (head[1] * grid_size < 0):
        return True
    return False

pygame.init()

grid_size = 25

# Set the number of tiles
num_tiles_x, num_tiles_y = 31, 31

# Set the screen size
width, height = num_tiles_x * grid_size, num_tiles_y * grid_size
screen = pygame.display.set_mode((width, height))

current_apple_x = grid_size * random.randint(0, num_tiles_x - 1) + 3
current_apple_y = grid_size * random.randint(0, num_tiles_y - 1) + 3

positions = [[16, 16]]

def main():
    Apple_Eaten = False
    score = 0
    direction = [1, 0]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, height))

        # Flow of game rendering
        append_positions(positions, Apple_Eaten, direction)
        Draw_Apple(Apple_Eaten)
        Apple_Eaten = False
        Draw_Grid()
        print_snake(positions, score)

        # Movement vector input handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != [1, 0]:
            direction = [-1, 0]
        elif keys[pygame.K_RIGHT] and direction != [-1, 0]:
            direction = [1, 0]
        elif keys[pygame.K_UP] and direction != [0, 1]:
            direction = [0, -1]
        elif keys[pygame.K_DOWN] and direction != [0, -1]:
            direction = [0, 1]

        # Check every frame for whether the apple has been eaten
        if positions[0][0] * grid_size + 3 == current_apple_x and positions[0][1] * grid_size + 3 == current_apple_y:
            Apple_Eaten = True
            score += 1
        
        # Check every frame whether a collision has occured
        if check_collision(positions):
            running = False

        pygame.display.flip()
        pygame.time.delay(80)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
