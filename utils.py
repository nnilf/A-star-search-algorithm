import math
import pygame
from constants import Colors

def get_clicked_pos(pos: tuple, rows: int, width: int, difference: int) -> tuple[int, int]:
    """Gets the row and column of where the mouse has clicked.

    Args:
        pos: Mouse position, x and y.
        rows: Rows within the grid.
        width: Width of the pygame window.
        difference: Vertical offset of the grid.

    Returns:
        Row and col of mouse position.
    """
    gap = width // rows
    x, y = pos

    if y < difference or x < 0 or x >= width:
        return None, None  # Click outside grid

    row = (y - difference) // gap
    col = x // gap

    if row >= rows or col >= rows:
        return None, None  # Click outside grid

    return row, col


def heuristic(node_coords: tuple[int, int], end_coords: tuple[int, int]) -> float:
    """Calculates the heuristic Fscore for the selected node using Euclidean distance

    Args:
        node: Tuple containig nodes coordinates.
        end: Tuple containing target nodes coordinates

    Returns:
        H score for current node
    """
    node_x, node_y = node_coords
    end_x, end_y = end_coords
    return math.sqrt((node_x - end_x) ** 2 + (node_y - end_y) ** 2)

def draw_grid(rows: int, width: int, win: pygame.Surface, difference: int):
    """Draws grid onto pygame window

    Args:
        rows: Amount of rows within the grid.
        width: Width of the pygame window.
        win: Pygame window.

    Returns:
        Lines that draw a grid on the pygame window
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Colors.GREY, (0, (i * gap) + difference), (width, (i * gap) + difference))
        for j in range(rows):
            pygame.draw.line(win, Colors.GREY, (j * gap, difference), (j * gap, width+difference))