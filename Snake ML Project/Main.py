import pygame
import sys
from game_functions import GameState
from Pathfinding import createStateArray, createStartEndNodes, astar

def main():
    game_state = GameState(num_tiles_x=31, num_tiles_y=31, grid_size=25)

    Apple_Eaten = False
    score = 0
    direction = [1, 0]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.rect(game_state.screen, (0, 0, 0), (0, 0, game_state.width, game_state.height))

        # Flow of game rendering
        game_state.append_positions(Apple_Eaten, direction)
        game_state.Draw_Apple(Apple_Eaten)
        Apple_Eaten = False
        game_state.Draw_Grid()
        game_state.print_snake(score)
        createStateArray(game_state)
        createStartEndNodes(game_state.positions[0], game_state.current_apple_x, game_state.current_apple_y)
        # Create a function that highlights the current path

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
        if game_state.positions[0][0] * game_state.grid_size + 3 == game_state.current_apple_x and game_state.positions[0][1] * game_state.grid_size + 3 == game_state.current_apple_y:
            Apple_Eaten = True
            score += 1

        # Check every frame whether a collision has occurred
        if game_state.check_collision():
            running = False

        pygame.display.flip()
        pygame.time.delay(80)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
