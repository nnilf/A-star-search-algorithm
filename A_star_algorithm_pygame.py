from queue import PriorityQueue
import pygame
import math
from typing import List, Callable
 
# intialise Pygame
pygame.init()
 
# intialise Width
HEIGHT = 920
GRID_WIDTH = 880
DIFFERENCE = HEIGHT - GRID_WIDTH

# intialise surface
WIN = pygame.display.set_mode((GRID_WIDTH, HEIGHT))
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
    def __init__(self, x: int, y: int, width: int, total_rows: int, difference: int):
        self.width = width
        self.row = x
        self.col = y
        self.children = []
        self.colour = WHITE
        self.total_rows = total_rows
        self.difference = difference

    def draw(self, win: pygame.Surface):
        """Draws current node onto grid"""
        pygame.draw.rect(win, self.colour, (self.col * self.width, self.row * self.width + self.difference, self.width, self.width))

    def set_path(self):
        self.colour = BLUE

    def checked(self):
        return self.colour == RED
    
    def checking(self):
        return self.colour == GREEN
    
    def set_checked(self):
        self.colour = RED

    def set_checking(self):
        self.colour = GREEN

    def get_coords(self):
        return (self.row, self.col)
    
    def set_start(self):
        self.colour = CYAN
    
    def set_end(self):
        self.colour = MAGENTA
        
    def set_barrier(self):
        self.colour = BLACK
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def reset(self):
        self.colour = WHITE

    def get_children(self):
        return self.children
    
    def update_children(self, grid: list[list["Node"]], grid_size: int) -> None:
        """
        Gets the children of current element which is all the Nodes next to the current node

        :param grid: grid of nodes
        :param grid_size: size of the grid
        :returns children: all the children of the current element
        """
        self.children = []  # Reset children

        directions = [(1,0), (-1,0), (0,1), (0,-1), (-1,-1), (1,-1), (1,1), (-1,1)]
        for dx, dy in directions:
            nx, ny = self.row + dx, self.col + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not grid[nx][ny].is_barrier():
                self.children.append(grid[nx][ny])

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))
    

def heuristic(node_coords: tuple[int, int], end_coords: tuple[int, int]) -> float:
    """
    Calculates the heuristic Fscore for the selected node using Euclidean distance

    :param node: Tuple containig nodes coordinates
    :param end: Tuple containing target nodes coordinates
    :returns: H score for current node
    """
    node_x, node_y = node_coords
    end_x, end_y = end_coords
    return math.sqrt((node_x - end_x) ** 2 + (node_y - end_y) ** 2)


def create_grid(grid_size: int, width: int, difference: int) -> List[List[Node]]:
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
            grid[i].append(Node(i, j, gap, grid_size, difference))

    return grid


def create_path(came_from: Node, current: Node, draw: Callable[[], None]):
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



def algorithm(start: Node, end: Node, grid: list[list[Node]], draw: Callable[[], None]) -> bool:
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
    
    
def draw_grid(rows: int, width: int, win: pygame.Surface, difference: int):
    """
    Draws grid onto pygame window

    :param rows: amount of rows within the grid
    :param width: width of the pygame window
    :param win: pygame window
    :returns: lines that draw a grid on the pygame window
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, (i * gap) + difference), (width, (i * gap) + difference))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, difference), (j * gap, width+difference))


def draw(grid: list[list[Node]], rows: int, win: pygame.Surface, width: int, difference: int):
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

    draw_grid(rows, width, win, difference)
    pygame.display.update()


def get_clicked_pos(pos: tuple, rows: int, width: int, difference: int) -> tuple[int, int]:
    """
    Gets the row and column of where the mouse has clicked

    :param pos: mouse position, x and y
    :param rows: rows within the grid
    :param width: width of the pygame window
    :param difference: vertical offset of the grid
    :returns: row and col of mouse position
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


def calculate(width: int, win: pygame.Surface, difference: int):
    """
    Main algorithm function

    :param width: width of pygame window
    :param win: pygame window
    """
    grid_size = 44
    grid = create_grid(grid_size, width, difference)
    running = True

    start = None
    end = None

    while running:

        # draw grid
        draw(grid, grid_size, win, width, difference)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                running = False

            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, grid_size, width, difference)
                if row < grid_size and col < grid_size:
                    if row is not None and col is not None:
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
                row, col = get_clicked_pos(pos, grid_size, width, difference)
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
                    grid = create_grid(grid_size, width, difference)

                if event.key == pygame.K_SPACE:
                    if event.key == pygame.K_SPACE:
                        for row in grid:
                            for node in row:
                                # Clear previous path, checking, and checked nodes but keep barriers
                                if (node.colour == BLUE or  
                                    node.colour == RED or   
                                    node.colour == GREEN):  
                                    node.reset()            
                                
                                node.update_children(grid, grid_size)
                        
                        # restore start and end visuals if they exist
                        if start:
                            start.set_start()
                        if end:
                            end.set_end()
                        
                        # Run algorithm
                        algorithm(start, end, grid, lambda: draw(grid, grid_size, win, width, difference))

    pygame.quit()

calculate(GRID_WIDTH, WIN, DIFFERENCE)