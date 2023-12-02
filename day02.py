from aoc import non_blank_lines, print_assert
import re

gid = re.compile(r'Game (\d+)')
red = re.compile(r'(\d+) red')
green = re.compile(r'(\d+) green')
blue = re.compile(r'(\d+) blue')

def find_max(p, line):
    found = re.findall(p, line)
    return max([int(s) for s in found]) if found else 0

def part_1(lines):
    def test(line):
        return find_max(red, line) <= 12 and find_max(green, line) <= 13 and find_max(blue, line) <= 14

    return sum([find_max(gid, line) for line in lines if test(line)])

def part_2(lines):
    return sum([find_max(red, line) * find_max(green, line) * find_max(blue, line) for line in lines])

lines = non_blank_lines("input/day02.txt")
print_assert("Part 1:", part_1(lines), 2476)
print_assert("Part 2:", part_2(lines), 54911)
