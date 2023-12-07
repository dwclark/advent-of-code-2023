from aoc import non_blank_lines, print_assert
import re
import math

pnum = re.compile(r'\d+')
lines = non_blank_lines("input/day06.txt")
times = [int(s) for s in re.findall(pnum, lines[0])]
distances = [int(s) for s in re.findall(pnum, lines[1])]
the_time = int("".join([str(n) for n in times]))
the_distance = int("".join([str(n) for n in distances]))

def num_ways(time, distance):
    def first():
        for my_time in range(1, time):
            total_distance = my_time * (time - my_time)
            if total_distance > distance:
                return my_time

    def last():
        for my_time in reversed(range(1, time)):
            total_distance = my_time * (time - my_time)
            if total_distance > distance:
                return my_time

    return last() - first() + 1

print_assert("Part 1:", math.prod([num_ways(time, distance) for time, distance in zip(times,distances)]), 741000)
print_assert("Part 2:", num_ways(the_time, the_distance), 38220708)
