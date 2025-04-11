import pygame
from constants import Display, Algorithm
from visualiser import create_grid, draw, get_clicked_pos, clear_path_and_update_children
from A_star_algorithm import algorithm

def main():
    pygame.init()
    WIN = pygame.display.set_mode((Display.GRID_WIDTH, Display.WINDOW_HEIGHT))
    pygame.display.set_caption("A* Path Finding Algorithm")
    
    grid = create_grid(Algorithm.DEFAULT_GRID_SIZE, Display.GRID_WIDTH, Display.DIFFERENCE)
    start, end = None, None

    running = True
    while running:
        draw(grid, Algorithm.DEFAULT_GRID_SIZE, WIN, Display.GRID_WIDTH, Display.DIFFERENCE)
        
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
                    grid = clear_path_and_update_children(grid, Algorithm.DEFAULT_GRID_SIZE, start, end)
                    algorithm(start, end, grid, lambda: draw(grid, Algorithm.DEFAULT_GRID_SIZE, WIN, Display.GRID_WIDTH, Display.DIFFERENCE))

    pygame.quit()

if __name__ == "__main__":
    main()