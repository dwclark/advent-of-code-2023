from aoc import blank_line_grouped, print_assert
import re
import portion

p = p = re.compile(r'-| ')
pnum = re.compile(r'\d+')

class Mapping:
    def __init__(self):
        self.srcs = []
        self.dests = []

    def __repr__(self):
        return f"srcs: {self.srcs}, dests {self.dests}"

    def add(self, dest_start, src_start, length):
        self.srcs.append(portion.closedopen(src_start, src_start + length))
        self.dests.append(portion.closedopen(dest_start, dest_start + length))

    def mapped_values(self, intervals):
        outputs = []
        for interval in intervals:
            leftover = interval
            for src_interval, dest_interval in zip(self.srcs, self.dests):
                overlap = leftover & src_interval
                leftover = leftover - overlap
                if not overlap.empty:
                    for to_process in list(overlap):
                        width = to_process.upper - to_process.lower
                        shift = to_process.lower - src_interval.lower
                        if width == 0:
                            outputs.append(portion.singleton(dest_interval.lower + shift))
                        else:
                            outputs.append(portion.closedopen(dest_interval.lower + shift, dest_interval.lower + shift + width))
            outputs.extend(list(leftover))
        return outputs

def make_mapping(group):
    ary = re.split(p, group[0])
    m = Mapping()
    for line in group[1:]:
        nums = [int(s) for s in re.findall(pnum, line)]
        m.add(*nums)
    return m

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def solve(mappings, intervals):
    def do_mapping(val):
        n = val
        for m in mappings:
            n = m.mapped_values(n)
        return n

    all_intervals = []
    for interval in intervals:
        all_intervals.extend(do_mapping(interval))

    return min([interval.lower for interval in all_intervals])
        
groups = blank_line_grouped('input/day05.txt')
mappings = [make_mapping(group) for group in groups[1:]]
seeds = [int(s) for s in re.findall(pnum, groups[0][0])]
seeds_1 = [ portion.singleton(seed) for seed in seeds ]
seeds_2 = [portion.closedopen(v1, v1+length) for v1, length in pairwise(seeds)]

print_assert("Part 1:", solve(mappings, seeds_1), 240320250)
print_assert("Part 2:", solve(mappings, seeds_2),  28580589)


