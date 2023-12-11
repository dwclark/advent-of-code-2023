from aoc import non_blank_lines, print_assert
import heapq

def blank_rows(grid):
    return [ i for i, row in enumerate(grid) if all([s == '.' for s in row]) ]

def blank_cols(grid):
    return [ col for col in range(0, len(grid[0])) if all([row[col] == '.' for row in grid]) ]

def expand_grid(grid, rows, cols):
    lists = [list(row) for row in grid]
    accum = []
    for list_row in lists:
        new_row = []
        for col, letter in enumerate(list_row):
            if col in cols:
                new_row.extend(['.', '.'])
            else:
                new_row.append(letter)
        accum.append(''.join(new_row))

    ret_accum = []
    for row, contents in enumerate(accum):
        if row in rows:
            ret_accum.extend(['.' * len(contents)] * 2)
        else:
            ret_accum.append(contents)
    return ret_accum

def neighbors(coord):
    row, col = coord
    return [ (row+1, col), (row-1, col), (row, col+1), (row, col-1) ]

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
            ret[tuple(sorted([start_at, node]))] = dist
        for neighbor in neighbors(node):
            if in_grid(grid, neighbor):
                add_coord(neighbor, dist+1)
    return ret

def distances(grid):
    ret = {}
    for row, contents in enumerate(grid):
        for col, letter in enumerate(contents):
            if letter == '#':
                ret.update(bfs(grid, (row, col)))
    return ret

grid = non_blank_lines('input/day11.txt')
expanded = expand_grid(grid, blank_rows(grid), blank_cols(grid))
print(sum(distances(expanded).values()))
