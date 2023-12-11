from aoc import non_blank_lines, print_assert
import heapq

multiplier = None
blank_rows = None
blank_cols = None

def find_blank_rows(grid):
    return [ i for i, row in enumerate(grid) if all([s == '.' for s in row]) ]

def find_blank_cols(grid):
    return [ col for col in range(0, len(grid[0])) if all([row[col] == '.' for row in grid]) ]

def neighbors(coord):
    row, col = coord
    def up():
        if row + 1 in blank_rows:
            return (multiplier + 1, (row + 2, col))
        else:
            return (1, (row + 1, col))

    def down():
        if row - 1 in blank_rows:
            return (multiplier + 1, (row - 2, col))
        else:
            return (1, (row - 1, col))
        
    def left():
        if col -  1 in blank_cols:
            return (multiplier + 1, (row, col - 2))
        else:
            return (1, (row, col - 1))
        
    def right():
        if col + 1 in blank_cols:
            return (multiplier + 1, (row, col + 2))
        else:
            return (1, (row, col + 1))

    return [ up(), down(), left(), right() ]

def in_grid(grid, coord):
    max_row = len(grid)
    max_col = len(grid[0])
    row, col = coord
    return 0 <= row and row < max_row and 0 <= col and col < max_col
        
def bfs(grid, start_at):
    queue = []
    finder = {}

    def should_add(coord, dist):
        if not coord in finder:
            return True

        entry = finder[coord]
        prev_dist, prev_coord, processed = entry
        if prev_dist <= dist:
            return False

        entry[2] = True
        return True
    
    def add_coord(coord, dist):
        if should_add(coord, dist):
            entry = [dist, coord, False]
            heapq.heappush(queue, entry)
            finder[coord] = entry

    def get_next():
        while queue:
            entry = heapq.heappop(queue)
            dist, coord, processed = entry
            if not processed:
                entry[2] = True
                return (entry[0], entry[1])
        return None

    ret = {}
    add_coord(start_at, 0)
    while entry := get_next():
        dist, node = entry
        row, col = node
        
        if grid[row][col] == '#' and node != start_at:
            #print(f"found # at {node}")
            ret[tuple(sorted([start_at, node]))] = dist
        for neighbor in neighbors(node):
            add_dist, new_coord = neighbor
            if in_grid(grid, new_coord):
                add_coord(new_coord, dist + add_dist)
    return ret

def distances(grid):
    ret = {}
    for row, contents in enumerate(grid):
        for col, letter in enumerate(contents):
            if letter == '#':
                ret.update(bfs(grid, (row, col)))
    return ret

grid = non_blank_lines('input/day11.txt')
blank_rows = set(find_blank_rows(grid))
blank_cols = set(find_blank_cols(grid))
multiplier = 1000000
print(blank_rows)
print(blank_cols)
print(sum(distances(grid).values()))
