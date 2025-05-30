from dataclasses import dataclass

@dataclass
class Colors:
    # UI colors
    WHITE = (255, 255, 255)  # Background
    BLACK = (0, 0, 0)        # Barriers
    GREY = (190, 190, 190)   # Grid lines
    
    # Algorithm state colors
    RED = (255, 0, 0)        # Checked nodes
    GREEN = (0, 255, 0)      # Nodes being checked
    BLUE = (0, 0, 255)       # Final path
    
    # Special node colors
    CYAN = (0, 255, 255)     # Start node
    MAGENTA = (255, 0, 255)  # End node
    YELLOW = (255, 255, 0)   # Optional highlighting

@dataclass
class Display:
    WINDOW_HEIGHT = 940
    GRID_WIDTH = 792
    DIFFERENCE = WINDOW_HEIGHT - GRID_WIDTH

@dataclass
class Algorithm:
    DEFAULT_GRID_SIZE = 44