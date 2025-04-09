import numpy as np
from queue import PriorityQueue
import pygame
 
# intialise Pygame
pygame.init()
 
# intialise Width
width = 880

# intialise surface
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Path Finding Algorithm")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (190, 190, 190)

class Node:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._coord_x = x * width
        self._coord_y = y * width
        self._start = False
        self._end = False
        self._g_score = np.inf
        self._h_score = np.inf
        self._f_score = np.inf
        self._children = []
        self._parent = None
        self._colour = white

    def draw(self, win):
        pygame.draw.rect(win, self._colour, (self._coord_x, self._coord_y, width, width))

    def get_colour(self):
        return self._colour

    def checked(self):
        return self._colour == red
    
    def checking(self):
        return self._colour == green

    def get_coords(self):
        return (self._x, self._y)
    
    def get_parent(self):
        return self._parent
    
    def update_f_score(self):
        self._f_score = self._g_score + self._h_score
    
    def get_f_score(self):
        return self._f_score

    def get_g_score(self):
        return self._g_score
    
    def set_g_score(self, value):
        self._g_score = value

    def set_parent(self, node):
        self._parent = node
    
    def set_start(self):
        if not(self._end):
            self._start = True
            self._g_score = 0
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
            return "Node is start or end node"
        
    def is_start(self):
        return self._start
    
    def is_end(self):
        return self._end
    
    def is_barrier(self):
        return self._colour == black
    
    def reset(self):
        self._start = False
        self._end = False
        self._barrier = False
    
    def get_children(self, grid, grid_size):
        """
        Gets the children of current element which is all the Nodes next to the current node

        :param grid: grid of nodes
        :param grid_size: size of the grid
        :returns children: all the children of the current element
        """
        self._children = []  # Reset children

        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = self._x + dx, self._y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not grid[nx][ny].is_barrier():
                self._children.append(grid[nx][ny])

        return self._children

    def heuristic(self, end):
        """
        Calculates the heuristic Fscore for the selected node using manhattan calculation

        :param end: ending node
        :returns: Sets H-score for node
        """
        end_x, end_y = end.get_coords()
        self._h_score = (abs(self._x - end_x) + abs(self._y - end_y))

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

def create_grid(grid_size):
    """
    Intialises a grid of node classes
    
    :param grid_size: size of the grid to be made
    :returns grid: grid with intialised nodes
    """
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Node(i, j))

    return grid

def create_path(start, end, prior_node):
    """
    Loop through path elements and add them to array

    :param start: starting node
    :param end: target node
    :param prior_node: node prior to reaching the target node
    :returns path: quickest path to go from start node to end node
    """
    finished = False
    path = []
    path.append(end.get_coords())
    node = prior_node
    while not finished:
        if node == start:
            finished = True
        path.append(node.get_coords())
        node = node.get_parent()
        
    path.reverse()
    print(path)

def algorithm(start, end, grid, grid_size):
    """A* path finding algorithm

    :param start: start node
    :param end: end node
    :param grid: grid of nodes
    :param grid_size: size of the grid
    :returns: output of quickest path
    """
    goal_found = False
    queue = PriorityQueue()
    closed_list = set()
    open_list = set()

    start.set_g_score(0)

    queue.put((start.get_g_score(), start))
    open_list.add(start)

    while not(queue.empty()):
        current_node = queue.get()[1]
        open_list.remove(current_node)

        if current_node == end:
            print('solution found')
            goal_found = True
            create_path(start, end, current_node.get_parent())

        closed_list.add(current_node)
        children = current_node.get_children(grid, grid_size)

        for child in children:

            if child.is_barrier() or child in closed_list:
                continue

            tentative_g = current_node.get_g_score() + 1

            if child not in open_list or tentative_g < child.get_g_score():
                child.set_g_score(tentative_g)
                child.heuristic(end)
                child.update_f_score()
                child.set_parent(current_node)

                if child not in open_list:
                    queue.put((child.get_f_score(), child))
                    open_list.add(child)

    if not goal_found:
        print("No path found")
        return ()
    
def draw_grid(rows):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))

def draw(grid, rows):
	win.fill(white)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(rows)
	pygame.display.update()

def calculate():
    running = True

    while running:

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                running = False

        grid_size = 44
        grid = create_grid(grid_size)

        draw(grid, grid_size)

        # start = grid[0][0]
        # end = grid[4][4]

        # start.set_start()
        # end.set_end()

        # algorithm(start, end, grid, grid_size)

    pygame.quit()

calculate()