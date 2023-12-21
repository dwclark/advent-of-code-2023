from aoc import blank_line_grouped, print_assert
import re
import copy

preg = re.compile(r'([a-zA-Z]+)([<|>])(\d+):([a-zA-Z]+)')
ppart = re.compile(r'([a-z])=(\d+)')

class Expression:
    def __init__(self, components):
        self.rating = components[0]
        self.op = components[1]
        self.amount = int(components[2])
        self.target = components[3]

    def __repr__(self):
        return f"{self.rating}{self.op}{self.amount}:{self.target}"

    def __str__(self):
        return self.__repr__()

    def is_match(self, part):
        if self.op == '<':
            return part[self.rating] < self.amount
        elif self.op == '>':
            return part[self.rating] > self.amount
        
class Rule:
    def __init__(self, s):
        self.expressions = []

        bracket = s.find('{')
        self.name = s[0:bracket]
        rest = s[bracket+1:len(s)-1]
        raw_rules = rest.split(',')
        
        for raw_rule in raw_rules:
            if raw_rule.find(':') != -1:
                components = re.findall(preg, raw_rule)
                self.expressions.append(Expression(components[0]))
            else:
                self.default = raw_rule

    def __repr__(self):
        return self.name + '{' + ','.join([f"{e}" for e in self.expressions]) + f",{self.default}}}"
    
    def eval(self, part):
        for expr in self.expressions:
            if expr.is_match(part):
                return expr.target
        return self.default
    
class Part:
    def __init__(self, line):
        self.dictionary = { tup[0]:int(tup[1]) for tup in re.findall(ppart, line) }

    def __getitem__(self, key):
        return self.dictionary[key]

    def __repr__(self):
        return self.dictionary.__repr__()

    def total(self):
        return sum(self.dictionary.values())
        
def make_rules(lines):
    return { r.name:r for r in [Rule(line) for line in lines] }

def make_parts(lines):
    return list([Part(line) for line in lines])

def evaluate(rules, parts):
    accepted = []
    output = 'in'
    finished = set(['A', 'R'])
    
    for part in parts:
        while not output in finished:
            output = rules[output].eval(part)
        if output == 'A':
            accepted.append(part)
        output = 'in'

    return sum([a.total() for a in accepted])

groups = blank_line_grouped('input/day19.txt')
rules = make_rules(groups[0])
parts = make_parts(groups[1])
print_assert("Part1:", evaluate(rules, parts), 374873)
