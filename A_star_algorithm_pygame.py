class Quadrant:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._start = False
        self._end = False
        self._barrier = False

    def get_coords(self):
        return (self._x, self._y)
    
    def set_start(self):
        if not(self._end):
            self._start = True
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
        
def create_grid():
    grid = []
    for i in range(5):
        grid.append([])
        for j in range(5):
            grid[i].append(Quadrant(i, j))

    return grid

def main():
    grid = create_grid()

    start = grid[0][0]
    end = grid[4][4]

    start.set_start
    end.set_end
