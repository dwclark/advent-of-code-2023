from aoc import non_blank_lines, print_assert
from collections import deque

# row, col
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)
VERTICAL = set([NORTH, SOUTH])
HORIZONTAL = set([EAST, WEST])
FORWARD_SLASH = { NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH }
BACKWARD_SLASH = { NORTH: WEST, WEST: NORTH, SOUTH: EAST, EAST: SOUTH }
TO_STR = { NORTH: 'N', SOUTH: 'S', EAST: 'E', WEST: 'W' }

def grid_legal(grid, at):
    return at[0] >= 0 and at[1] >= 0 and at[0] < len(grid) and at[1] < len(grid[0])

def add_history(history, beams):
    keep = []
    for b in beams:
        prev = history.get(b.at)
        if prev and not b.direction in prev:
            prev.append(b.direction)
            keep.append(b)
        elif not prev:
            history[b.at] = [b.direction]
            keep.append(b)
    return keep

class Beam:
    def __init__(self, direction, at):
        self.direction = direction
        self.at = at

    def __repr__(self):
        return f"{self.at} {TO_STR[self.direction]}"
    
    def beam(self, direction):
        return Beam(direction, (self.at[0] + direction[0], self.at[1] + direction[1]))
    
    def do_split(self, ret, dirs):
        for tup in dirs:
            ret.append(self.beam(tup))

    def next(self, grid):
        char = grid[self.at[0]][self.at[1]]
        tmp = []

        if char == '.' or (char == '-' and self.direction in HORIZONTAL) or (char == '|' and self.direction in VERTICAL):
            tmp.append(self.beam(self.direction))
        elif char == '|' and self.direction in HORIZONTAL:
            self.do_split(tmp, VERTICAL)
        elif char == '-' and self.direction in VERTICAL:
            self.do_split(tmp, HORIZONTAL)
        elif char == '/':
            tmp.append(self.beam(FORWARD_SLASH[self.direction]))
        elif char == '\\':
            tmp.append(self.beam(BACKWARD_SLASH[self.direction]))
        else:
            raise Exception("should not be here")

        return list([b for b in tmp if grid_legal(grid, b.at)])

def find_energy(grid, start):
    dq = deque([start])
    history = {}
    add_history(history, [start])
    
    while(len(dq) > 0):
        beam = dq.popleft()
        beams = beam.next(grid)
        dq.extend(add_history(history, beams))

    return len(history)

def part_1(grid):
    return find_energy(grid, Beam(EAST, (0, 0)))

def part_2(grid):
    beams = []
    for row in range(0, len(grid)):
        beams.append(Beam(EAST, (row, 0)))
        beams.append(Beam(WEST, (row, len(grid[0]) - 1)))

    for col in range(0, len(grid[0])):
        beams.append(Beam(SOUTH, (0, col)))
        beams.append(Beam(NORTH, (len(grid) - 1, col)))

    return max([find_energy(grid, b) for b in beams])

grid = non_blank_lines('input/day16.txt')
print_assert("Part 1:", part_1(grid), 6795)
print_assert("Part 2:", part_2(grid), 7154)
