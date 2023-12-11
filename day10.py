from aoc import non_blank_lines, print_assert
from collections import deque

directions = {'|': lambda cur: [ (cur[0]+1, cur[1]), (cur[0]-1, cur[1]) ],
              '-': lambda cur: [ (cur[0], cur[1]-1), (cur[0], cur[1]+1) ],
              'L': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]+1) ],
              'J': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]-1) ],
              '7': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]-1) ],
              'F': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]+1) ],
              '.': lambda cur: [] }

vertical = set([ '|', 'L', 'J', '7', 'F' ])
change_direction = set([ 'L', 'J', '7', 'F' ])
up_direction = set(['L', 'J'])
down_direction = set(['F', '7'])

class Grid:
    def __init__(self, grid, start_at):
        self.grid = grid
        self.start_at = start_at
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __getitem__(self, key):
        return self.grid[key[0]][key[1]]

    def __contains__(self, coord):
        return coord[0] >= 0 and coord[0] < len(self.grid) and coord[1] >= 0 and coord[1] < len(self.grid[0])

def bfs(grid):
    to_visit = deque()
    to_visit.append((grid.start_at, 0))
    visited = {}
    while len(to_visit) != 0:
        node = to_visit.popleft()
        location = node[0]
        dist = node[1]
        visited[location] = dist
        letter = grid[location]
        for possible in directions[letter](location):
            if not possible in visited:
                to_visit.append((possible, dist+1))

    return visited

def is_inside(grid, loop, coord):
    crosses = 0
    last_cd = None
    row = coord[0]
    for col in range(coord[1]+1, grid.cols):
        current_coord = (row, col)
        letter = grid[current_coord] if current_coord in loop else '.'
        if letter == '|':
            crosses = crosses + 1
        elif letter in change_direction:
            if not last_cd:
                last_cd = letter
            else:
                if ((last_cd in up_direction and letter in down_direction) or
                    (last_cd in down_direction and letter in up_direction)):
                    crosses = crosses + 1
                last_cd = None
              
        #elif not horizontal_run and letter in change_direction:
        #    horizontal_run = True
        #elif horizontal_run and letter in change_direction:
        #    crosses = crosses + 1
        #    horizontal_run = False

    if crosses % 2 == 1:
        print(f"{coord} is inside")
        return True
    else:
        return False

def num_inside(grid, loop):
    total = 0
    for row in range(0, grid.rows):
        for col in range(0, grid.cols):
            coord = (row, col)
            if not coord in loop and is_inside(grid, loop, coord):
                total = total + 1
    return total
        
#grid = Grid(non_blank_lines('input/day10sa.txt'), (1, 1))
#grid = Grid(non_blank_lines('input/day10sb.txt'), (0, 2))
#grid = Grid(non_blank_lines('input/day10.txt'), (128, 89))
#loop = bfs(grid)
#print(max(loop.values()))
#grid = Grid(non_blank_lines('input/day10sd.txt'), (1,1))
#grid = Grid(non_blank_lines('input/day10se.txt'), (4,12))
grid = Grid(non_blank_lines('input/day10.txt'), (128, 89))
loop = bfs(grid)
#print(num_inside(grid, loop))

