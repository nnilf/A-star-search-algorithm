import math
import pygame
from constants import Colors
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


def heuristic(node_coords: tuple[int, int], end_coords: tuple[int, int]) -> float:
    """Calculates the heuristic Fscore for the selected node using Euclidean distance"""
    node_x, node_y = node_coords
    end_x, end_y = end_coords
    return math.sqrt((node_x - end_x) ** 2 + (node_y - end_y) ** 2)


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

def draw_grid(rows: int, width: int, win: pygame.Surface, difference: int):
    """Draws grid onto pygame window"""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Colors.GREY, (0, (i * gap) + difference), (width, (i * gap) + difference))
        for j in range(rows):
            pygame.draw.line(win, Colors.GREY, (j * gap, difference), (j * gap, width+difference))


def clear_path_and_update_children(grid, grid_size, start, end):
    """Clear visualization nodes and update node connections"""
    for row in grid:
        for node in row:
            if (node.colour == Colors.BLUE or node.colour == Colors.RED or node.colour == Colors.GREEN):
                node.set_state("reset")
            node.update_children(grid, grid_size)
    
    if start:
        start.set_state("start")
    if end:
        end.set_state("end")
    
    return grid