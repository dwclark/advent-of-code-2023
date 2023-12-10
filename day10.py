from aoc import non_blank_lines, print_assert
from collections import deque

directions = {'|': lambda cur: [ (cur[0]+1, cur[1]), (cur[0]-1, cur[1]) ],
              '-': lambda cur: [ (cur[0], cur[1]-1), (cur[0], cur[1]+1) ],
              'L': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]+1) ],
              'J': lambda cur: [ (cur[0]-1, cur[1]), (cur[0], cur[1]-1) ],
              '7': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]-1) ],
              'F': lambda cur: [ (cur[0]+1, cur[1]), (cur[0], cur[1]+1) ] }
class Grid:
    def __init__(self, grid, start_at):
        self.grid = grid
        self.start_at = start_at

    def __getitem__(self, key):
        return self.grid[key[0]][key[1]]

def bfs_max(grid):
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

    return max(visited.values())
        
#grid = Grid(non_blank_lines('input/day10sa.txt'), (1, 1))
#grid = Grid(non_blank_lines('input/day10sb.txt'), (0, 2))
grid = Grid(non_blank_lines('input/day10.txt'), (128, 89))
print(bfs_max(grid))
