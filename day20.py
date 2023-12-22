from aoc import non_blank_lines, print_assert
from collections import deque
from enum import Enum
import math
import re

class Magnitude(Enum):
    LOW = 0
    HIGH = 1

    def __repr__(self):
        return 'low' if self.value == 0 else 'high'

class Pulse:
    def __init__(self, source, destination, magnitude):
        self.source = source
        self.destination = destination
        self.magnitude = magnitude

class Module:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    def recv(self, bus):
        return None

    def add_input(self, val):
        pass

    def send(self, bus, magnitude):
        for output in self.outputs:
            bus.send(Pulse(self.name, output, magnitude))

class FlipFlop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.on = False

    def __repr__(self):
        return f"%{self.name} -> " + ', '.join(self.outputs)
    
    def recv(self, bus):
        pulse = bus.take()
        if pulse.magnitude == Magnitude.LOW:
            if not self.on:
                self.on = True
                self.send(bus, Magnitude.HIGH)
            else:
                self.on = False
                self.send(bus, Magnitude.LOW)

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.inputs = {}
        self.debug = False
        self.first_high = {}

    def add_input(self, val):
        self.inputs[val] = Magnitude.LOW
        self.first_high[val] = -1

    def __repr__(self):
        return ', '.join(self.inputs) + ' -> ' + f"&{self.name}" + ' -> ' + ', '.join(self.outputs)

    def recv(self, bus):
        pulse = bus.take()

        if self.debug:
            was = self.inputs[pulse.source]
            new = pulse.magnitude
            if was == Magnitude.LOW and new == Magnitude.HIGH:
                print(f"{bus.button_presses} {pulse.source} from low -> high")
                
        self.inputs[pulse.source] = pulse.magnitude

        if all([m == Magnitude.HIGH for m in self.inputs.values()]):
            self.send(bus, Magnitude.LOW)
        else:
            self.send(bus, Magnitude.HIGH)
        
class Broadcaster(Module):
    def __init__(self, outputs):
        super().__init__('broadcaster', outputs)

    def __repr__(self):
        return f"broadcaster -> " + ', '.join(self.outputs)
    
    def recv(self, bus):
        pulse = bus.take()
        assert pulse.destination == self.name
        self.send(bus, Magnitude.LOW)

class Sink(Module):
    def __init__(self, name):
        super().__init__(name, [])
        self.low_pulses = 0

    def __repr__(self):
        return self.name

    def recv(self, bus):
        pulse = bus.take()
        if pulse.magnitude == Magnitude.LOW:
            self.low_pulses += 1

class Bus:
    def __init__(self):
        self.q = deque()
        self.low_pulses = 0
        self.high_pulses = 0
        self.button_presses = 0
        
    def next_module(self):
        if self.q:
            return self.q[0].destination
        else:
            return None
        
    def take(self):
        return self.q.popleft()

    def send(self, pulse):
        self.q.append(pulse)
        if pulse.magnitude == Magnitude.LOW:
            self.low_pulses += 1
        else:
            self.high_pulses += 1

    def press_button(self):
        self.send(Pulse('button', 'broadcaster', Magnitude.LOW))
        self.button_presses += 1

def make_module(line):
    src, outputs = line.split(' -> ')
    src = src.strip()
    outputs = [ o.strip() for o in outputs.split(',') ]
    if src == 'broadcaster':
        return Broadcaster(outputs)
    elif src.find('%') == 0:
        return FlipFlop(src[1:], outputs)
    elif src.find('&') == 0:
        return Conjunction(src[1:], outputs)
    else:
        return Sink(src[1:])

def wire_inputs(modules):
    to_add = {}
    for module in modules.values():
        for output in module.outputs:
            if modules.get(output) is None and to_add.get(output) is None:
                to_add[output] = Sink(output)
                
    modules.update(to_add)
    
    for module in modules.values():
        for output in module.outputs:
            modules[output].add_input(module.name)

def part_1(modules):
    bus = Bus()
    
    for time in range(0, 1000):
        bus.press_button()
        while n := bus.next_module():
            modules[n].recv(bus)

    return bus.low_pulses * bus.high_pulses

def part_2(modules):
    #when all inputs to ls (the only input to rx) are high
    #then it will send a single low to rx. The following
    #are the times when a button press results in a
    #high being set for each of the inputs to ls, therefore
    #the lcm of those presses will the first time rx is low

    #enable debug mode for the ls module and then kill it after
    #you see repeats for each of the inputs (at least one repeat)
    #to see how often each module flips to high

    #Somewhat proud of myself that I figure this day out without
    #looking at hints. This is much less than it could have been
    #had I not taken so long.
    
    # bus = Bus()
    # ls = modules['ls']
    # ls.debug = True
    
    # while True:
    #     bus.press_button()
    #     while n := bus.next_module():
    #         modules[n].recv(bus)
    return math.lcm(3779, 3889, 3907, 4051)


modules = { m.name:m for m in [ make_module(line) for line in non_blank_lines("input/day20.txt") ] }
wire_inputs(modules)
print_assert("Part 1:", part_1(modules), 869395600)
print_assert("Part 2:", part_2(modules), 232605773145467)

    
