from queue import PriorityQueue
import math
from typing import Callable
from Node import Node


# Persistent algorithm state
algorithm_state = {
    'open_set': None,
    'came_from': None,
    'g_score': None,
    'f_score': None,
    'open_set_hash': None,
    'count': 0,
    'initialized': False
}

def init_algorithm(start: Node, end: Node, grid: list[list[Node]], is_eight_directional: bool):
    """Initialize or reset algorithm state"""
    algorithm_state['open_set'] = PriorityQueue()
    algorithm_state['open_set'].put((0, 0, start))
    algorithm_state['came_from'] = {}
    algorithm_state['g_score'] = {node: float("inf") for row in grid for node in row}
    algorithm_state['g_score'][start] = 0
    algorithm_state['f_score'] = {node: float("inf") for row in grid for node in row}
    algorithm_state['f_score'][start] = heuristic(start.get_coords(), end.get_coords(), is_eight_directional)
    algorithm_state['open_set_hash'] = {start}
    algorithm_state['count'] = 0
    algorithm_state['initialized'] = True

def algorithm_step(start: Node, end: Node, grid: list[list[Node]], draw: Callable[[], None], is_eight_directional: bool) -> bool:
    """Execute one step of A* algorithm"""
    if not algorithm_state['initialized']:
        init_algorithm(start, end, grid, is_eight_directional)
    
    if algorithm_state['open_set'].empty():
        return True
    
    # Process current node
    current = algorithm_state['open_set'].get()[2]
    algorithm_state['open_set_hash'].remove(current)
    
    if current == end:
        create_path(algorithm_state['came_from'], end, draw)
        end.set_state("end")
        start.set_state("start")
        return True
    
    # Process neighbors
    for child in current.get_children():
        dx = abs(child.row - current.row)
        dy = abs(child.col - current.col)
        move_cost = math.sqrt(2) if dx + dy == 2 else 1
        tentative_g = algorithm_state['g_score'][current] + move_cost
        
        if tentative_g < algorithm_state['g_score'][child]:
            algorithm_state['came_from'][child] = current
            algorithm_state['g_score'][child] = tentative_g
            algorithm_state['f_score'][child] = tentative_g + heuristic(
                child.get_coords(), end.get_coords(), is_eight_directional)
            
            if child not in algorithm_state['open_set_hash']:
                algorithm_state['count'] += 1
                algorithm_state['open_set'].put((algorithm_state['f_score'][child], 
                                               algorithm_state['count'], child))
                algorithm_state['open_set_hash'].add(child)
                child.set_state("checking")
    
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