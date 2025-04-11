from constants import Colors
import pygame

class Node:
    def __init__(self, x: int, y: int, width: int, total_rows: int, difference: int):
        self.width = width
        self.row = x
        self.col = y
        self.children = []
        self.colour = Colors.WHITE
        self.total_rows = total_rows
        self.difference = difference

    def set_state(self, state: str):
        COLOUR_MAP = {
            "checking": Colors.GREEN,
            "checked": Colors.RED,
            "path": Colors.BLUE,
            "start": Colors.CYAN,
            "end": Colors.MAGENTA,
            "barrier": Colors.BLACK,
            "reset": Colors.WHITE
        }
        self.colour = COLOUR_MAP[state]

    def draw(self, win: pygame.Surface):
        """Draws current node onto grid"""
        pygame.draw.rect(win, self.colour, (self.col * self.width, self.row * self.width + self.difference, self.width, self.width))

    def checked(self):
        return self.colour == Colors.RED
    
    def checking(self):
        return self.colour == Colors.GREEN
    
    def get_coords(self):
        return (self.row, self.col)
    
    def is_barrier(self):
        return self.colour == Colors.BLACK

    def get_children(self):
        return self.children
    
    def update_children(self, grid: list[list["Node"]], grid_size: int) -> None:
        """Gets the children of current element which is all the Nodes next to the current node.

        Args:
            grid: Grid of nodes.
            grid_size: Size of the grid.

        Returns:
            children: Children of the current element
        """
        self.children = []  # Reset children

        # directions (N, E, S, W)
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        
        # (no corner checking needed)
        for dx, dy in directions:
            nx, ny = self.row + dx, self.col + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not grid[nx][ny].is_barrier():
                self.children.append(grid[nx][ny])
        
        # diagonal directions 
        diagonal_directions = [(-1,-1), (1,-1), (1,1), (-1,1)]
        
        # Check diagonal directions with corner validation
        for dx, dy in diagonal_directions:
            nx, ny = self.row + dx, self.col + dy
            
            # First ensure diagonal position is valid and not a barrier
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not grid[nx][ny].is_barrier():
                # Check that we're not cutting across a corner
                # Both adjacent cells must be passable for diagonal movement to be allowed
                adjacent1 = grid[self.row][ny]  # Horizontally adjacent
                adjacent2 = grid[nx][self.col]  # Vertically adjacent
                
                # Only allow diagonal movement if at least one adjacent cell is passable
                if not adjacent1.is_barrier() or not adjacent2.is_barrier():
                    self.children.append(grid[nx][ny])

    def __lt__(self, other: "Node"):
        return True

    def __eq__(self, other: "Node"):
        if not isinstance(other, Node):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))