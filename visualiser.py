import pygame
import time
from constants import Colors, Display
from Node import Node

def create_grid(grid_size: int, width: int, difference: int) -> list[list[Node]]:
    """Intialises a grid of node classes"""
    gap = width // grid_size
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Node(i, j, gap, grid_size, difference))
    return grid


def draw_toggle_button(win: pygame.Surface, is_eight_directional: bool):
    """Draws a button on the screen to toggle between 4 and 8 directional movement."""
    pygame.draw.rect(win, Colors.GREY, (10, 10, 185, 110))
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Toggle Movement:", True, Colors.WHITE)
    movement = font.render(f"{'Euclidean' if is_eight_directional else 'Manhattan'} Distance", True, Colors.WHITE)
    win.blit(text, (15, 20))
    win.blit(movement, (15, 80))


def draw_grid(rows: int, width: int, win: pygame.Surface, difference: int):
    """Draws grid onto pygame window"""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Colors.GREY, (0, (i * gap) + difference), (width, (i * gap) + difference))
        for j in range(rows):
            pygame.draw.line(win, Colors.GREY, (j * gap, difference), (j * gap, width+difference))


def draw(grid: list[list[Node]], rows: int, win: pygame.Surface, width: int, difference: int, is_eight_directional: bool, elapsed_time: float, start: Node = None, end: Node = None):
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

    draw_toggle_button(win, is_eight_directional)

    # Draw timer on the screen
    font = pygame.font.SysFont("arial", 20)

    instruction_text = ""
    if start is None:
        instruction_text = "Click to place START node"
    elif end is None:
        instruction_text = "Click to place END node"

    # Position in top right (adjust coordinates as needed)
    text_surface = font.render(instruction_text, True, Colors.RED)
    text_rect = text_surface.get_rect(topright=(width -145, 10))
    win.blit(text_surface, text_rect)

    # Draw instructions on the screen
    instructions = [
        "Instructions:",
        "Space - Start Pathfinding",
        "C - Clear Grid",
        "Left Click - Set Start/End/Barrier",
        "Right Click - Reset Node",
        "Toggle Button - Switch Movement"
    ]
    for i, line in enumerate(instructions):
        if i >= 3:
            instruction_text = font.render(line, True, Colors.BLACK)
            win.blit(instruction_text, (450, 40 + (i-3) * 25))
        else:
            instruction_text = font.render(line, True, Colors.BLACK)
            win.blit(instruction_text, (200, 40 + i * 25))

    timer_text = font.render(f"Time Elapsed: {elapsed_time:.2f}s", True, Colors.BLACK)
    win.blit(timer_text, (200, 10))

    pygame.display.flip()


def get_clicked_pos(pos: tuple, rows: int, width: int, difference: int) -> tuple[int, int]:
    """Gets the row and column of where the mouse has clicked"""
    gap = width // rows
    x, y = pos

    if y < difference or x < 0 or x >= width:
        return None, None  # Click outside grid

    row = (y - difference) // gap
    col = x // gap

    if row >= rows or col >= rows:
        return None, None  # Click outside grid

    return row, col


def clear_path_and_update_children(grid, grid_size, start, end, is_eight_directional):
    """Clear visualization nodes and update node connections"""
    for row in grid:
        for node in row:
            if (node.colour == Colors.BLUE or node.colour == Colors.RED or node.colour == Colors.GREEN):
                node.set_state("reset")
            node.update_children(grid, grid_size, is_eight_directional)
    
    if start:
        start.set_state("start")
    if end:
        end.set_state("end")
    
    return grid


def check_toggle_button_click(pos: tuple) -> bool:
    """Checks if the toggle button is clicked"""
    button_rect = pygame.Rect(10, 10, 185, 110)
    return button_rect.collidepoint(pos)