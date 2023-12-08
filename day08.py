from aoc import blank_line_grouped, print_assert
import re
import math

def locate(directions, instructions, start, func):
    counter = 0
    key = start
    value = ''
    while not func(key):
        value = instructions[key]
        direction = directions[counter % len(directions)]
        key = value[0] if direction == 'L' else value[1]
        counter = counter + 1
    return counter

def part_2(directions, instructions):
    keys = list([ s for s in instructions.keys() if s.endswith('A') ])
    func = lambda s: s.endswith('Z')
    counters = [ locate(directions, instructions, key, func) for key in keys ]
    return math.lcm(*counters)
    
pline = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')
groups = blank_line_grouped('input/day08.txt')
directions = groups[0][0]
instructions = { m[1]: (m[2],m[3]) for m in [ re.match(pline, line) for line in groups[1] ] } 

print_assert("Part 1:", locate(directions, instructions, 'AAA', lambda s: s == 'ZZZ'), 21251)
print_assert("Part 2:", part_2(directions, instructions), 11678319315857)
