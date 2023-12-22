from aoc import blank_line_grouped, print_assert
import re
import copy
import portion
from functools import reduce
from operator import and_
import math
from abc import ABC, abstractmethod

preg = re.compile(r'([a-zA-Z]+)([<|>])(\d+):([a-zA-Z]+)')
ppart = re.compile(r'([a-z])=(\d+)')

def add_portion(so_far, rating, portion):
    ret = { **so_far }
    ret[rating] = ret[rating] & portion
    return ret

def any_empty(so_far):
    for p in so_far.values():
        if p.empty:
            return True
    return False

class Rule:
    def __init__(self, rating, op, amount, workflow):
        self.rating = rating
        self.op = op
        self.amount = int(amount)
        self.workflow = workflow
        self.interval = portion.closedopen(1, self.amount) if self.op == '<' else portion.closedopen(self.amount+1, 4001)

    def __repr__(self):
        return f"{self.rating}{self.op}{self.amount}:{self.workflow} ({self.interval})"

    def __str__(self):
        return self.__repr__()

    def eval_part(self, workflows, part):
        if part[self.rating] in self.interval:
            return workflows[self.workflow].eval_part(workflows, part)
        else:
            return None

    def flip(self):
        if self.op == '<':
            return Rule(self.rating, '>', self.amount-1, self.workflow)
        else:
            return Rule(self.rating, '<', self.amount+1, self.workflow)

    def count_possible(self, workflows, so_far):
        n = add_portion(so_far, self.rating, self.interval)
        if any_empty(n):
            return 0
        else:
            return workflows[self.workflow].count_possible(workflows, n)

class Fixed(Rule):
    def __init__(self, workflow):
        self.workflow = workflow
        
    def __repr__(self):
        return f"{self.workflow}"

    def __str__(self):
        return self.workflow

    def eval_part(self, workflows, part):
        if self.workflow in 'AR':
            return self.workflow
        else:
            return workflows[self.workflow].eval_part(workflows, part)

    def count_possible(self, workflows, so_far):
        if self.workflow == 'A':
            return math.prod([(p.upper - p.lower) for p in so_far.values()])
        elif self.workflow == 'R':
            return 0
        else:
            return workflows[self.workflow].count_possible(workflows, so_far)

def make_rule(raw_rule):
    components = re.findall(preg, raw_rule)
    if components:
        return Rule(*components[0])
    else:
        return Fixed(raw_rule)

class Workflow:
    def __init__(self, s):
        self.rules = []
        bracket = s.find('{')
        self.name = s[0:bracket]
        rest = s[bracket+1:len(s)-1]
        self.rules = list([make_rule(s) for s in rest.split(',')])

    def __repr__(self):
        return self.name + '{' + ','.join([f"{r}" for r in self.rules])
    
    def eval_part(self, workflows, part):
        for rule in self.rules:
            if next_wf := rule.eval_part(workflows, part):
                return next_wf

    def count_possible(self, workflows, so_far):
        total = 0
        for rule in self.rules:
            total += rule.count_possible(workflows, so_far)
            if not isinstance(rule, Fixed):
                so_far = add_portion(so_far, rule.rating, rule.flip().interval)
        return total
    
class Part:
    def __init__(self, line):
        self.dictionary = { tup[0]:int(tup[1]) for tup in re.findall(ppart, line) }

    def __getitem__(self, key):
        return self.dictionary[key]

    def __repr__(self):
        return self.dictionary.__repr__()

    def total(self):
        return sum(self.dictionary.values())
        
def make_workflows(lines):
    fixed = { 'A': Fixed('A'), 'R': Fixed('R') }
    return fixed | { w.name:w for w in [Workflow(line) for line in lines] }

def make_parts(lines):
    return list([Part(line) for line in lines])

groups = blank_line_grouped('input/day19.txt')
workflows = make_workflows(groups[0])
parts = make_parts(groups[1])

print_assert("Part 1:", sum([p.total() for p in parts if workflows['in'].eval_part(workflows, p) == 'A']), 374873)
print_assert("Part 2:", workflows['in'].count_possible(workflows, { s:portion.closedopen(1, 4001) for s in 'xmas' }), 122112157518711)
