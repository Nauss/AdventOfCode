from collections import Counter
from pathlib import Path

class Hand:
    cards = ""
    rank = 0
    bid = 0

    def __init__(self, input):
        self.cards = input[0]
        self.bid = int(input[1])
        self.rank()

    def __str__(self):
        return f"cards: {self.cards}, rank: {self.rank}, bid: {self.bid}"

    def rank(self):
        s = sorted(Counter(self.cards).values(), reverse=True)
        rank = self.rank
        if s[0] == 5:
            rank= 7
        elif s[0] == 4:
            rank= 6
        elif s[0] == 3:
            if s[1] == 2:
                rank= 5
            else:
                rank= 4
        elif s[0] == 2:
            if s[1] == 2:
                rank= 3
            else:
                rank= 2
        else:
            rank= 1
        self.rank = rank

def comparison(a, b):
    if a.rank == b.rank:
        return a.cards > b.cards
    return a.rank > b.rank

def part1(hands):
    result = sorted(hands, key=comparison, reverse=True)
    return hands

path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    hands = [Hand(line.strip().split()) for line in lines]
    result = part1(hands)
    print("part1: ", result)
    # result = part2(lines)
    # print("part2: ", result)