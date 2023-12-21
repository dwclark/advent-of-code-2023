from aoc import non_blank_lines, print_assert
import re
from enum import Enum

class Corner(Enum):
    INNER = 1
    OUTER = 2

CORNERS = {('L','U'): Corner.OUTER, ('L','D'): Corner.INNER, ('R','U'): Corner.INNER, ('R','D'): Corner.OUTER,
           ('U','L'): Corner.INNER, ('D','L'): Corner.OUTER, ('U','R'): Corner.OUTER, ('D','R'): Corner.INNER}
TRANSLATE = { 'R': (1,0), 'D': (0,-1), 'L': (-1,0), 'U': (0,1) }
HORIZONTAL = set(['R', 'L'])
VERTICAL = set(['U', 'D'])

def add(start, direction, move_by):
    factor = TRANSLATE[direction]
    to_move = (move_by * factor[0], move_by * factor[1])
    return (start[0] + to_move[0], start[1] + to_move[1])

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"[{self.start} {self.end}]"

    def is_horizontal(self):
        return self.start[1] == self.end[1]

class Border:
    def __init__(self, start, inst):
        self.start = start
        self.distance = self.decode_distance(inst)
        self.direction = self.decode_direction(inst)
        self.end = add(start, self.direction, self.distance)

    def __repr__(self):
        return f"{self.direction} {self.start} --> {self.end}"

    def decode_distance(self, inst):
        return int(inst[1])

    def decode_direction(self, inst):
        return inst[0]

    def get_squares(self):
        return abs((self.start[0] - self.end[0]) + (self.start[1] - self.end[1]))

    def is_horizontal(self):
        return self.direction in HORIZONTAL

class Border2(Border):
    def decode_distance(self, inst):
        s = inst[2]
        return int(s[1:len(s)-1], base=16)

    def decode_direction(self, inst):
        s = inst[2]
        i = int(s[len(s)-1:])
        return list(TRANSLATE.keys())[i]

def make_borders(instructions, clazz):
    start = (0,0)
    ret = []
    for inst in instructions:
        b = clazz(start, inst)
        ret.append(b)
        start = b.end
    return ret

def bottom_horizontal(borders):
    min_index, min_b = (None, None)
    for index, b in enumerate(borders):
        if b.is_horizontal() and (min_b is None or b.end[1] < min_b.end[1]):
            min_index = index
            min_b = b
    return (min_index, min_b)

def to_lines(borders):
    ret = []
    start = (0,0)

    for index, c in enumerate(borders):
        #these next four lines too me forever to figure out
        #the main idea is to trace a line on the outer edge of the border
        #the trick is how long to draw the line based on which types
        #of corners are at the edge of the lines. Basicall
        # 2 outer corners: add 1
        # 1 inner, 1 outer: add 0
        # 2 inner: add -1
        p = borders[index-1]
        n = borders[index+1] if index + 1 < len(borders) else borders[0]
        corners = [ CORNERS[(p.direction, c.direction)], CORNERS[(c.direction, n.direction)] ]
        correction = corners.count(Corner.OUTER) - 1
        end = add(start, c.direction, c.distance + correction)
        ret.append(Line(start, end))
        start = end
    return ret

def area_under(lines):
    area = 0
    for line in lines:
        if line.is_horizontal():
            area = area + ((line.end[0] - line.start[0]) * line.start[1])
    return abs(area)

p = re.compile(r'([RDLU]) (\d+) \((#[0-9a-f]{6})\)')
lines = non_blank_lines('input/day18.txt')
instructions = [ re.findall(p, line)[0] for line in lines ]

print_assert("Part 1:", area_under(to_lines(make_borders(instructions, Border))), 74074)
print_assert("Part 2:", area_under(to_lines(make_borders(instructions, Border2))), 112074045986829)
