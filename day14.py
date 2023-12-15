from aoc import non_blank_lines, print_assert
import copy

def tilt_north(grid):
    for row in range(1, len(grid)):
        for col in range(0, len(grid[0])):
            if grid[row][col] == 'O':
                final = row
                for rev in range(row-1, -1, -1):
                    if grid[rev][col] == '.':
                        final = rev
                    else:
                        break
                grid[row][col] = '.'
                grid[final][col] = 'O'
    return grid

def tilt_south(grid):
    for row in range(len(grid)-1, -1, -1):
        for col in range(0, len(grid[0])):
            if grid[row][col] == 'O':
                final = row
                for rev in range(row+1, len(grid)):
                    if grid[rev][col] == '.':
                        final = rev
                    else:
                        break
                grid[row][col] = '.'
                grid[final][col] = 'O'
    return grid

def tilt_west(grid):
    for col in range(1, len(grid[0])):
        for row in range(0, len(grid)):
            if grid[row][col] == 'O':
                final = col
                for rev in range(col-1, -1, -1):
                    if grid[row][rev] == '.':
                        final = rev
                    else:
                        break
                grid[row][col] = '.'
                grid[row][final] = 'O'
    return grid

def tilt_east(grid):
    for col in range(len(grid[0]) - 1, -1, -1):
        for row in range(0, len(grid)):
            if grid[row][col] == 'O':
                final = col
                for rev in range(col+1, len(grid[0])):
                    if grid[row][rev] == '.':
                        final = rev
                    else:
                        break
                grid[row][col] = '.'
                grid[row][final] = 'O'
    return grid

def compute_weight(grid):
    return sum([row.count('O') * (len(grid) - index) for index, row in enumerate(grid)])

def for_storage(grid):
    return '\n' + '\n'.join(["".join(inner) for inner in grid])

def cycle(grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)

def repeat_info(grid):
    index = 0
    d = {}

    while True:
        cycle(grid)
        index = index + 1
        storage = for_storage(grid)
        if storage in d:
            return [d[storage], index, d ]
        else:
            d[storage] = index

def part_2(grid):
    original = copy.deepcopy(grid)
    info = repeat_info(grid)
    cycle_start = info[0]
    cycle_repeat = info[1]
    cycle_length = cycle_repeat - cycle_start
    times = (1000000000 - cycle_start) // cycle_length
    offset = 1000000000 - (cycle_start + (times * cycle_length))

    for i in range(0, info[0] + offset):
        cycle(original)
    return compute_weight(original)

grid = [list(line) for line in non_blank_lines('input/day14.txt')]
print_assert("Part 1:", compute_weight(tilt_north(copy.deepcopy(grid))), 108759)
print_assert("Part 2:", part_2(grid), 89089)
