from queue import PriorityQueue
import math
from typing import Callable
from Node import Node


def algorithm(start: Node, end: Node, grid: list[list[Node]], draw: Callable[[], None], is_eight_directional: bool) -> bool:
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
    f_score[start] = heuristic(start.get_coords(), end.get_coords(), is_eight_directional)

    open_set_hash = {start}

    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            create_path(came_from, end, draw)
            end.set_state("end")
            start.set_state("start")
            return True
        
        draw()
        
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
                f_score[child] = tentative_g + heuristic(child.get_coords(), end.get_coords(), is_eight_directional)
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


def heuristic(node_coords: tuple[int, int], end_coords: tuple[int, int], is_eight_directional: bool) -> float:
    """Calculates the heuristic Fscore for the selected node using Euclidean distance"""
    node_x, node_y = node_coords
    end_x, end_y = end_coords
    
    if is_eight_directional:
        # Using Euclidean distance for 8-directional movement
        return math.sqrt((node_x - end_x) ** 2 + (node_y - end_y) ** 2)
    else:
        # Using Manhattan distance for 4-directional movement
        return abs(node_x - end_x) + abs(node_y - end_y)