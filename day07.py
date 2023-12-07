from aoc import non_blank_lines, print_assert
import re
from operator import itemgetter

to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9,
          '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2 }

to_num_joker = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10, '9': 9,
                '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2 }

def to_rank_common(d):
    if len(d) == 1:
        return 7
    elif len(d) == 2 and 4 in d.values():
        return 6
    elif len(d) == 2 and 3 in d.values():
        return 5
    elif len(d) == 3 and 3 in d.values():
        return 4
    elif len(d) == 3 and 2 in d.values():
        return 3
    elif len(d) == 4:
        return 2
    elif len(d) == 5:
        return 1
    else:
        raise Exception("can't handle dictionary")

def to_rank_regular(num_cards):
    d = {}
    for card in num_cards:
        d[card] = d.get(card, 0) + 1
    return to_rank_common(d)

def to_rank_joker(num_cards):
    d = {}
    for card in num_cards:
        if card != 1:
            d[card] = d.get(card, 0) + 1

    if len(d) == 0:
        return 7
    
    key = next(reversed(sorted(d.items(), key=lambda tup: tup[1])))[0]
    d[key] = d[key] + num_cards.count(1)
    return to_rank_common(d)

class Hand:
    def __init__(self, cards, bid):
        self.bid = int(bid)
        self.do_ranks(cards)

    def do_ranks(self, cards):
        self.cards = [to_num[letter] for letter in cards]
        self.rank = to_rank_regular(self.cards)
        self.all_ranks = [self.rank] + self.cards

    def __repr__(self):
        return f"({self.cards}, {self.rank}, {self.bid})"

    def sorting(self):
        return itemgetter(0,1,2,3,4,5)(self.all_ranks)

class JokerHand(Hand):
    def do_ranks(self, cards):
        self.cards = [to_num_joker[letter] for letter in cards]
        self.rank = to_rank_joker(self.cards)
        self.all_ranks = [self.rank] + self.cards

def find_score(hands):
    sorted_hands = list(sorted(hands, key=lambda hand: hand.sorting()))
    scores = [ hand.bid * (1+index) for index, hand in enumerate(sorted_hands) ]
    return sum(scores)

lines = non_blank_lines("input/day07.txt")
hands = [ Hand(*args) for args in [ line.split(' ') for line in lines ] ]
joker_hands = [ JokerHand(*args) for args in [ line.split(' ') for line in lines ] ]

print_assert("Part 1:", find_score(hands), 255048101)
print_assert("Part 2:", find_score(joker_hands), 253718286)
