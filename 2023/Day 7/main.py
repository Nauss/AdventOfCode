from collections import Counter
from pathlib import Path
from operator import itemgetter
import functools

order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
order_part2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
is_part2 = False


class Hand:
    cards = ""
    rank = 0
    bid = 0

    def __init__(self, input):
        self.cards = input[0]
        self.bid = int(input[1])
        s = sorted(Counter(self.cards).values(), reverse=True)
        rank = 0
        if s[0] == 5:
            rank = 7
        elif s[0] == 4:
            rank = 6
        elif s[0] == 3:
            if s[1] == 2:
                rank = 5
            else:
                rank = 4
        elif s[0] == 2:
            if s[1] == 2:
                rank = 3
            else:
                rank = 2
        else:
            rank = 1
        self.rank = rank

    def __repr__(self):
        return f"cards: {self.cards}, rank: {self.rank}, bid: {self.bid}"

    def part2(self):
        counts = Counter(
            self.cards,
        )
        s = sorted(
            counts.items(),
            key=itemgetter(1),
            reverse=True,
        )
        if "J" in self.cards:
            if s[0][0] != "J":
                counts[s[0][0]] += counts["J"]
                counts["J"] = 0
            elif len(s) > 1:
                counts[s[1][0]] += counts["J"]
                counts["J"] = 0
        s = sorted(
            counts.values(),
            reverse=True,
        )
        rank = 0
        if s[0] == 5:
            rank += 7
        elif s[0] == 4:
            rank += 6
        elif s[0] == 3:
            if s[1] == 2:
                rank += 5
            else:
                rank += 4
        elif s[0] == 2:
            if s[1] == 2:
                rank += 3
            else:
                rank += 2
        else:
            rank += 1
        self.rank = rank


def compare(hand1, hand2):
    actual_order = order_part2 if is_part2 else order
    if hand1.rank == hand2.rank:
        for i, c in enumerate(hand1.cards):
            if actual_order.index(c) > actual_order.index(hand2.cards[i]):
                return 1
            elif actual_order.index(c) < actual_order.index(hand2.cards[i]):
                return -1
        return 0
    elif hand1.rank > hand2.rank:
        return 1
    else:
        return -1


def part1(hands):
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare))
    result = 0
    for i, h in enumerate(sorted_hands):
        result += h.bid * (i + 1)

    return result


def part2(hands):
    [hand.part2() for hand in hands]
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare))
    result = 0
    for i, h in enumerate(sorted_hands):
        result += h.bid * (i + 1)

    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    hands = [Hand(line.strip().split()) for line in lines]
    result = part1(hands)
    is_part2 = True
    print("part1: ", result)
    result = part2(hands)
    print("part2: ", result)
