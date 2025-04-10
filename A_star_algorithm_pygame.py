import numpy as np
from queue import PriorityQueue
import pygame
 
# intialise Pygame
pygame.init()
 
# intialise Width
WIDTH = 968

# intialise surface
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)

class Node:
    def __init__(self, x, y, width, total_rows):
        self._width = width
        self._x = x
        self._y = y
        self._coords_x = x * width
        self._coords_y = y * width
        self._g_score = np.inf
        self._h_score = np.inf
        self._f_score = np.inf
        self._children = []
        self._parent = None
        self._colour = WHITE
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(win, self._colour, (self._coords_x, self._coords_y, self._width, self._width))

    def get_colour(self):
        return self._colour

    def checked(self):
        return self._colour == RED
    
    def checking(self):
        return self._colour == GREEN
    
    def set_checked(self):
        self._colour = RED

    def set_checking(self):
        self._colour = GREEN

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
        self._colour = CYAN
    
    def set_end(self):
        self._colour = MAGENTA
        
    def set_barrier(self):
        self._colour = BLACK
        
    def is_start(self):
        return self._colour == CYAN
    
    def is_end(self):
        return self._colour == MAGENTA
    
    def is_barrier(self):
        return self._colour == BLACK
    
    def reset(self):
        self._colour = WHITE
    
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
        if not isinstance(other, Node):
            return False
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))
    

def create_grid(grid_size, width):
    """
    Intialises a grid of node classes
    
    :param grid_size: size of the grid to be made
    :returns grid: grid with intialised nodes
    """
    gap = width // grid_size
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Node(i, j, gap, grid_size))

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
    
    
def draw_grid(rows, width, win):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(grid, rows, win, width):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(rows, width, win)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def calculate(width, win):
    grid_size = 44
    grid = create_grid(grid_size, width)
    running = True

    start = None
    end = None

    while running:

        # draw grid
        draw(grid, grid_size, win, width)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                running = False

            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, grid_size, width)
                if row < grid_size and col < grid_size:
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        node.set_start()

                    elif not end and node != start:
                        end = node
                        node.set_end()

                    elif node != start and node != end:
                        node.set_barrier()

            if pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, grid_size, width)
                if row < grid_size and col < grid_size:
                    node = grid[row][col]
                    node.reset()
                    start = None
                    end = None

            if event.type == pygame.KEYDOWN:
               
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(grid_size, width)


        # algorithm(start, end, grid, grid_size)

    pygame.quit()

calculate(WIDTH, WIN)