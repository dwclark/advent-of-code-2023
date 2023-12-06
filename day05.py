from aoc import blank_line_grouped, print_assert
import re

p = p = re.compile(r'-| ')
pnum = re.compile(r'\d+')

def overlap(tup1, tup2):
    if tup1[1] < tup2[0] or tup2[1] < tup1[0]:
        return None

    
class Mapping:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.srcs = []
        self.dests = []
        self.lengths = []

    def add(self, dest_start, src_start, length):
        self.srcs.append(src_start)
        self.dests.append(dest_start)
        self.lengths.append(length)

    def mapped_value(self, val):
        for index in range(0, len(self.srcs)):
            if self.srcs[index] <= val < (self.srcs[index] + self.lengths[index]):
                diff = val - self.srcs[index]
                return self.dests[index] + diff
        return val

    def mapped_range(self, tup):
        for index in range(0, len(self.srcs)):
            to_cmp = (self.srcs[index], self.srcs[index] + self.lengths[index])
            

def make_mapping(group):
    ary = re.split(p, group[0])
    m = Mapping(ary[0], ary[1])
    for line in group[1:]:
        nums = [int(s) for s in re.findall(pnum, line)]
        m.add(*nums)
    return m

def do_mapping(val, mappings):
    cur = val
    for m in mappings:
        cur = m.mapped_value(cur)
    return cur

def do_range_mapping(val, length):
    

groups = blank_line_grouped('input/day05.txt')
seeds = [int(s) for s in re.findall(pnum, groups[0][0])]
mappings = [make_mapping(group) for group in groups[1:]]

printAssert("Part 1:", min([do_mapping(seed, mappings) for seed in seeds]), 240320250)
