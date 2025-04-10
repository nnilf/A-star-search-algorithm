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
        self._children = []
        self._colour = WHITE
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(win, self._colour, (self._coords_x, self._coords_y, self._width, self._width))

    def set_path(self):
        self._colour = BLUE

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
    
    def set_start(self):
        self._colour = CYAN
    
    def set_end(self):
        self._colour = MAGENTA
        
    def set_barrier(self):
        self._colour = BLACK
    
    def is_barrier(self):
        return self._colour == BLACK
    
    def reset(self):
        self._colour = WHITE

    def get_children(self):
        return self._children
    
    def update_children(self, grid, grid_size):
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

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))
    

def heuristic(node, end):
    """
    Calculates the heuristic Fscore for the selected node using manhattan calculation

    :param node: current node to calculate from
    :param end: ending node
    :returns: H score for current node
    """
    node_x, node_y = node
    end_x, end_y = end
    return (abs(node_x - end_x) + abs(node_y - end_y))


def create_grid(grid_size, width):
    """
    Intialises a grid of node classes
    
    :param grid_size: size of the grid to be made
    :param width: width of pygame window
    :returns grid: grid with intialised nodes
    """
    gap = width // grid_size
    grid = []
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(Node(i, j, gap, grid_size))

    return grid


def create_path(came_from, current, draw):
    """
    Loop through path elements and add them to array

    :param came_from: set of nodes
    :param current: final/current node
    :param draw: draw function for when path is updated
    :returns path: drawn path
    """
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()



def algorithm(start, end, grid, draw):
    """
    A* path finding algorithm.

    :param start: Start node.
    :param end: End node.
    :param grid: Grid of nodes.
    :param draw: Function to update the GUI/visualizer.
    :return: True if path is found, False otherwise.
    """
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
            end.set_end()
            start.set_start()
            return True
        
        children = current.get_children()

        for child in children:
            tentative_g = g_score[current] + 1

            if tentative_g < g_score[child]:
                came_from[child] = current
                g_score[child] = tentative_g
                f_score[child] = tentative_g + heuristic(child.get_coords(), end.get_coords())
                if child not in open_set_hash:
                    count += 1
                    open_set.put((f_score[child], count, child))
                    open_set_hash.add(child)
                    child.set_checking()
        
        draw()

        if current != start:
            current.set_checked()
    
    return False
    
    
def draw_grid(rows, width, win):
    """
    Draws grid onto pygame window

    :param rows: amount of rows within the grid
    :param width: width of the pygame window
    :param win: pygame window
    :returns: lines that draw a grid on the pygame window
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(grid, rows, win, width):
    """
    Draws all nodes and updated pygame display from changes

    :param grid: grid full of nodes
    :param rows: rows within the grid
    :param win: pygame window
    :param width: width of the pygame window
    :returns: grid drawn onto pygame window
    """
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(rows, width, win)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Gets the row and column of where the mouse has clicked

    :param pos: mouse position, x and y
    :param rows: rows within the grid
    :param width: width of the pygame window
    :returns: row and col of mouse position
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def calculate(width, win):
    """
    Main algorithm function

    :param width: width of pygame window
    :param win: pygame window
    """
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
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
               
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(grid_size, width)

                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_children(grid, grid_size)

                    algorithm(start, end, grid, lambda: draw(grid, grid_size, win, width))


        # algorithm(start, end, grid, grid_size)

    pygame.quit()

calculate(WIDTH, WIN)