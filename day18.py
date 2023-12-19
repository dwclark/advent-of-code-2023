from aoc import non_blank_lines, print_assert
import re
from collections import deque

TRANSLATE = { 'R': (0,1), 'L': (0,-1), 'U': (-1,0), 'D': (1,0) }

def dig(instructions):
    s = set()
    pos = (0,0)
    s.add(pos)

    for inst in instructions:
        to_add = TRANSLATE[inst[0]]
        times = int(inst[1])
        for n in range(0, times):
            pos = ((pos[0] + to_add[0]), (pos[1] + to_add[1]))
            s.add(pos)
    return s
    
def count_interior(edges):
    interior = set()
    exterior = set()

    min_x = min(p[1] for p in edges) - 1
    max_x = max(p[1] for p in edges) + 1
    min_y = min(p[0] for p in edges) - 1
    max_y = max(p[0] for p in edges) + 1

    def bfs_categorize(coord):
        scheduled = set()
        stack = deque()
        stack.append(coord)
        scheduled.add(coord)
        
        while len(stack) > 0:
            element = stack.popleft()
            
            if element in interior:
                interior.add(coord)
                return
            elif element in exterior:
                exterior.add(coord)
                return
            elif element[1] < min_x or element[1] > max_x or element[0] < min_y or element[0] > max_y:
                exterior.add(coord)
                return

            for to_add in TRANSLATE.values():
                new = (to_add[0] + element[0], to_add[1] + element[1])
                if not new in edges and not new in scheduled:
                    stack.append(new)
                    scheduled.add(new)

        interior.add(coord)
    
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            coord = (y,x)
            if not coord in edges:
                bfs_categorize(coord)

    return interior

p = re.compile(r'([RDLU]) (\d+) \((#[0-9a-f]{6})\)')
lines = non_blank_lines('input/day18.txt')
instructions = [ re.findall(p, line)[0] for line in lines ]
s = dig(instructions)
interior = count_interior(s)
print(len(s | interior))
