from queue import PriorityQueue
import pygame
import math
from typing import List, Callable
from constants import Colors, Display, Algorithm 
from utils import create_grid, heuristic, get_clicked_pos, draw_grid, clear_path_and_update_children
from Node import Node

# intialise Pygame and surface
pygame.init()
WIN = pygame.display.set_mode((Display.GRID_WIDTH, Display.WINDOW_HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")


def calculate(width: int, win: pygame.Surface, difference: int, grid_size: int):
    """Main entry point for the A* visualization"""
    grid = create_grid(grid_size, width, difference)
    run_visualization_loop(grid, grid_size, win, width, difference)
    pygame.quit()


def algorithm(start: Node, end: Node, grid: list[list[Node]], draw: Callable[[], None]) -> bool:
    """A* path finding algorithm.

    Args:
        start: Start node.
        end: End node.
        grid: Grid of nodes.
        draw: Function to update the GUI/visualizer.

    Returns:
        True if path is found, False otherwise.
    """
    # Early return for invalid inputs
    if not start or not end:
        return False

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_coords(), end.get_coords())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            create_path(came_from, end, draw)
            end.set_state("end")
            start.set_state("start")
            return True
        
        children = current.get_children()

        for child in children:

            # Calculate whether this is a diagonal move
            dx = abs(child.row - current.row)
            dy = abs(child.col - current.col)
            # Diagonal moves cost more
            move_cost = math.sqrt(2) if dx + dy == 2 else 1

            tentative_g = g_score[current] + move_cost

            if tentative_g < g_score[child]:
                came_from[child] = current
                g_score[child] = tentative_g
                f_score[child] = tentative_g + heuristic(child.get_coords(), end.get_coords())
                if child not in open_set_hash:
                    count += 1
                    open_set.put((f_score[child], count, child))
                    open_set_hash.add(child)
                    child.set_state("checking")
        
        draw()

        if current != start:
            current.set_state("checked")
    
    return False


def create_path(came_from: dict[Node], current: Node, draw: Callable[[], None]):
    """Loop through path elements and add them to array

    Args:
        came_from: Set of nodes.
        current: Final/current node.
        draw: Draw function for when path is updated.

    Returns:
        path: Drawn path.
    """
    while current in came_from:
        current = came_from[current]
        current.set_state("path")
        draw()


def draw(grid: list[list[Node]], rows: int, win: pygame.Surface, width: int, difference: int):
    """Draws all nodes and updated pygame display from changes.

    Args:
        grid: Grid full of nodes.
        rows: Rows within the grid.
        win: Pygame window.
        width: Width of the pygame window.

    Returns:
        Grid drawn onto pygame window.
    """
    win.fill(Colors.WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(rows, width, win, difference)
    pygame.display.update()


def run_visualization_loop(grid: list[list[Node]], grid_size: int, win: pygame.Surface, 
                          width: int, difference: int) -> None:
    """Main loop for the visualization"""
    running = True
    start = None
    end = None

    while running:
        # Draw grid
        draw(grid, grid_size, win, width, difference)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            
            # Handle mouse and keyboard events
            running, grid, start, end = handle_input(event, grid, grid_size, start, end, width, difference)


def handle_input(event, grid, grid_size, start, end, width, difference):
    """Process user input events"""
    # Handle mouse clicks
    if pygame.mouse.get_pressed()[0]:  # left mouse button
        start, end = handle_left_click(grid, grid_size, start, end, width, difference)
    
    if pygame.mouse.get_pressed()[2]:  # right mouse button
        start, end = handle_right_click(grid, grid_size, start, end, width, difference)
    
    # Handle keyboard events
    if event.type == pygame.KEYDOWN:
        grid, start, end = handle_keyboard(event, grid, grid_size, start, end, width, difference)
    
    return True, grid, start, end  # Keep running by default


def handle_left_click(grid, grid_size, start, end, width, difference):
    """Process left mouse clicks to place start, end, and barriers"""
    pos = pygame.mouse.get_pos()
    row, col = get_clicked_pos(pos, grid_size, width, difference)
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
    return start, end


def handle_right_click(grid: list[list[Node]], grid_size: int, start: Node, end: Node, width: int, difference: int):
    """Process right mouse clicks to remove nodes"""
    pos = pygame.mouse.get_pos()
    row, col = get_clicked_pos(pos, grid_size, width, difference)
    if row is not None and col is not None:
        node = grid[row][col]
        node.set_state("reset")
        if node == start:
            start = None
        elif node == end:
            end = None
    return start, end


def handle_keyboard(event, grid, grid_size, start, end, width, difference):
    """Process keyboard inputs"""
    if event.key == pygame.K_c:
        start = None
        end = None
        grid = create_grid(grid_size, width, difference)
    
    if event.key == pygame.K_SPACE:
        # Clear previous path and update children in a single loop
        grid = clear_path_and_update_children(grid, grid_size, start, end)
        run_algorithm(grid, start, end, grid_size, width, difference)
    
    return grid, start, end


def create_grid(grid_size: int, width: int, difference: int) -> list[list[Node]]:
    """Intialises a grid of node classes

    Args:
        grid_size: Size of the grid to be made.
        width: Width of pygame window.

    Returns:
        grid: Grid with intialised nodes
    """
    gap = width // grid_size
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Node(i, j, gap, grid_size, difference))

    return grid


def run_algorithm(grid, start, end, grid_size, width, difference):
    """Execute the A* algorithm if start and end are defined"""
    if start and end:
        algorithm(start, end, grid, lambda: draw(grid, grid_size, WIN, width, difference))

calculate(Display.GRID_WIDTH, WIN, Display.DIFFERENCE, Algorithm.DEFAULT_GRID_SIZE)