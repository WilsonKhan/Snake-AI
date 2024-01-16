import pygame
import sys
from game_functions import GameState
from Pathfinding import createStateArray, createStartEndNodes, astar, findDirection

def main():
    game_state = GameState(num_tiles_x=20, num_tiles_y=20, grid_size=30)

    Apple_Eaten = False
    score = 0
    direction = [1, 0]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.rect(game_state.screen, (20, 20, 20), (0, 0, game_state.width, game_state.height))

        # Flow of game rendering
        game_state.append_positions(Apple_Eaten, direction)
        game_state.Draw_Apple(Apple_Eaten)
        Apple_Eaten = False
        game_state.Draw_Grid()
        game_state.print_snake(score)

        # Convert each position in the snake body to a tuple for comparison
        snake_body_for_astar = [tuple(pos) for pos in game_state.positions[1:]]  # Exclude the head

        start_node, end_node = createStartEndNodes(game_state.positions[0], game_state.current_apple_x, game_state.current_apple_y, game_state.grid_size)
        astar_path = astar(start_node, end_node, game_state.width, game_state.height, game_state.grid_size, snake_body_for_astar)
        print(astar_path)
        game_state.draw_astar_path(astar_path, game_state.grid_size)
        direction = findDirection(astar_path, game_state.positions[0])

        # Check every frame for whether the apple has been eaten
        if game_state.positions[0][0] * game_state.grid_size + 3 == game_state.current_apple_x and game_state.positions[0][1] * game_state.grid_size + 3 == game_state.current_apple_y:
            Apple_Eaten = True
            score += 1
            game_state.generate_new_apple()  # Generate a new apple
            
            # Check if the current A* path is empty (snake is trapped) or if it leads to the current apple position
            if not astar_path or astar_path[-1] != (game_state.current_apple_x, game_state.current_apple_y):

                # Recalculate A* path with the new apple position
                start_node, end_node = createStartEndNodes(game_state.positions[0], game_state.current_apple_x, game_state.current_apple_y, game_state.grid_size)
                astar_path = astar(start_node, end_node, game_state.width, game_state.height, game_state.grid_size, snake_body_for_astar)

        # Only update direction if the A* path is not empty
        if astar_path:
            direction = findDirection(astar_path, game_state.positions[0])

        # Check every frame if the snake is out of bounds or colliding with itself
            
        if game_state.check_collision():
            #running = False
            main()


        pygame.display.flip()
        pygame.time.delay(50)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
