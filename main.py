import pygame
import time
from constants import Display, Algorithm
from visualiser import create_grid, draw, get_clicked_pos, clear_path_and_update_children, check_toggle_button_click
from A_star_algorithm import algorithm

def main():
    pygame.init()
    WIN = pygame.display.set_mode((Display.GRID_WIDTH, Display.WINDOW_HEIGHT))
    pygame.display.set_caption("A* Path Finding Algorithm")
    
    grid = create_grid(Algorithm.DEFAULT_GRID_SIZE, Display.GRID_WIDTH, Display.DIFFERENCE)
    start, end = None, None
    is_eight_directional = True  # Initial setting: 8-directional (Euclidean)
    pathfinding_time = 0.0
    timer_active = False
    timer_start = 0
    final_time = None  

    running = True
    while running:

        current_time = time.time()
        if timer_active:
            pathfinding_time = current_time - timer_start

        display_time = final_time if final_time is not None else pathfinding_time

        draw(grid, Algorithm.DEFAULT_GRID_SIZE, WIN, Display.GRID_WIDTH, Display.DIFFERENCE, is_eight_directional, display_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse handling
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, Algorithm.DEFAULT_GRID_SIZE, Display.GRID_WIDTH, Display.DIFFERENCE)
                if row is not None and col is not None:
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        node.set_state("start")
                    elif not end and node != start:
                        end = node
                        node.set_state("end")
                    elif node != start and node != end:
                        node.set_state("barrier")

                # Handle toggle button click
                if check_toggle_button_click(pos):
                    is_eight_directional = not is_eight_directional
            
            if pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, Algorithm.DEFAULT_GRID_SIZE, Display.GRID_WIDTH, Display.DIFFERENCE)
                if row is not None and col is not None:
                    node = grid[row][col]
                    node.set_state("reset")
                    if node == start: start = None
                    elif node == end: end = None
            
            # Keyboard handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = end = None
                    grid = create_grid(Algorithm.DEFAULT_GRID_SIZE, Display.GRID_WIDTH, Display.DIFFERENCE)

                elif event.key == pygame.K_SPACE and start and end:

                    timer_start = time.time()
                    timer_active = True
                    final_time = None
                    pathfinding_time = 0.0

                    grid = clear_path_and_update_children(grid, Algorithm.DEFAULT_GRID_SIZE, start, end, is_eight_directional)
                    path_found = algorithm(start, end, grid, 
                                           lambda: draw(grid, Algorithm.DEFAULT_GRID_SIZE, WIN, Display.GRID_WIDTH, Display.DIFFERENCE,
                                             is_eight_directional, final_time if final_time is not None else (time.time() - timer_start))
                                             , is_eight_directional)

                    # If path was found, store the final time
                    if path_found:
                        final_time = time.time() - timer_start

    pygame.quit()

if __name__ == "__main__":
    main()