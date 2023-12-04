from aoc import non_blank_lines, print_assert
import re

p = p = re.compile(r':|\|')
pnum = re.compile(r'\d+')

class Card:
    def __init__(self, number, winners, on_card):
        self.number = number
        self.winners = winners
        self.on_card = on_card
        self.matched = len([ n for n in on_card if n in winners ])

def parse_cards(lines):
    cards = []
    for line in lines:
        groups = re.split(p, line)
        cards.append(Card(int(re.findall(pnum, groups[0])[0]), \
            [ int(s) for s in re.findall(pnum, groups[1]) ], \
            [ int(s) for s in re.findall(pnum, groups[2]) ]))
    return cards
        
def part_1(cards):
    return sum([ (2 ** (card.matched - 1) if card.matched > 0 else 0) for card in cards])

def part_2(cards):
    track = {card.number:1 for card in cards}
        
    for card in cards:
        if card.matched > 0:
            for i in range((card.number+1),(card.number+1+card.matched)):
                track[i] = track.get(i, 0) + track[card.number]
    return sum(track.values())

cards = parse_cards(non_blank_lines("input/day04.txt"))
print_assert("Part 1:", part_1(cards), 21138)
print_assert("Part 2:", part_2(cards), 7185540)
