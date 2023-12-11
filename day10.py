from aoc import non_blank_lines, print_assert
from collections import deque

directions = {'|': lambda cur: [ (cur[0]+1, cur[1]), (cur[0]-1, cur[1]) ],
              '-': lambda cur: [ (cur[0], cur[1]-1), (cur[0], cur[1]+1) ],
              'L': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]+1) ],
              'J': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]-1) ],
              '7': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]-1) ],
              'F': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]+1) ],
              '.': lambda cur: [] }

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

#Key to part 1: Just to a bfs walk of the pipes and extract
#the tile which has the highest number
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

#This is the key to part 2. The algorithm is called point-in-polygon. The
#wikipedia page for it is here: https://en.wikipedia.org/wiki/Point_in_polygon
#The only tricky part is figuring out when moving along horizontal pipes (-, F, L, 7, J)
#when we have entered/exited the shape. The insight is to recognize that
#only when they go the opposite direction have we entered the interior
#at some point. If they go the same direction (both up or down), then we have
#remained on the exterior.
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

    return crosses % 2 == 1

def num_inside(grid, loop):
    total = 0
    for row in range(0, grid.rows):
        for col in range(0, grid.cols):
            coord = (row, col)
            if not coord in loop and is_inside(grid, loop, coord):
                total = total + 1
    return total
        
grid = Grid(non_blank_lines('input/day10.txt'), (128, 89))
loop = bfs(grid)
print_assert("Part 1:", max(loop.values()), 6640)
print_assert("Part 2:", num_inside(grid, loop), 411)

