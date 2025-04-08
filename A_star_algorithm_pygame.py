import numpy as np
from queue import PriorityQueue

class Quadrant:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._start = False
        self._end = False
        self._barrier = False
        self._g_score = np.inf
        self._h_score = np.inf
        self._f_score = np.inf
        self._children = []

    def get_coords(self):
        return (self._x, self._y)
    
    def set_start(self):
        if not(self._end):
            self._start = True
            self._g_score = 0
            self._h_score = 0
            self._f_score = 0
        else:
            return "Already end node"
    
    def set_end(self):
        if not(self._start):
            self._end = True
        else:
            return "Already start node"
        
    def set_barrier(self):
        if not(self._start) and not(self._end):
            self._barrier = True
        else:
            return "Quadrant is start or end node"
        
    def is_start(self):
        return self._start
    
    def is_end(self):
        return self._end
    
    def is_barrier(self):
        return self._barrier
    
    def reset(self):
        self._start = False
        self._end = False
        self._barrier = False

    def get_children(self, grid, grid_size):
        if ((self._x + 1) < grid_size) and not(grid[self._x+1][self._y].is_barrier):
            self._children.append(grid[self._x+1][self._y])

        if ((self._x + - 1) < - 1) and not(grid[self._x-1][self._y].is_barrier):
            self._children.append(grid[self._x+1][self._y])

        if ((self._y + 1) < grid_size) and not(grid[self._x][self._y+1].is_barrier):
            self._children.append(grid[self._x][self._y+1])

        if ((self._y - 1) < - 1) and not(grid[self._x][self._y-1].is_barrier):
            self._children.append(grid[self._x][self._y-1])


def heuristic(end, quad):
    """
    Calculates the heuristic Fscore for the selected quadrant

    :param start: starting node
    :param end: ending node
    :param quad: node for calculations to applied from
    :returns: Fscore, Hscore, Gscore from calculations
    """
    quad_x, quad_y = quad.get_coords()
    end_x, end_y = end.get_coords()
    return (abs(quad_x - end_x) + abs(quad_y - end_y))


def create_grid(grid_size):
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Quadrant(i, j))

    return grid


def algorithm():
    queue = PriorityQueue()
    closed_list = []


def main():
    grid_size = 5
    grid = create_grid(grid_size)

    start = grid[0][0]
    end = grid[4][4]

    start.set_start
    end.set_end
