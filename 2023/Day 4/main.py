from pathlib import Path
import re
import copy

card = re.compile(r"Card +(\d+): (.*) \| (.*)")


def part1(line):
    matches = card.match(line)
    winners = re.split("\s+", matches.group(2))
    numbers = re.split("\s+", matches.group(3))
    win = set()
    for number in numbers:
        if number in winners:
            win.add(number)

    nbWins = len(win)
    if nbWins <= 2:
        return (nbWins, nbWins)
    worth = 1
    for i in range(nbWins - 1):
        worth = worth * 2
    return (worth, nbWins)


def part2(lines, winners):
    totalNbCards = 0
    cards = copy.deepcopy(lines)
    while len(cards):
        line = cards.pop(0)
        totalNbCards += 1
        cardIndex = int(card.match(line).group(1)) - 1
        for i in range(winners[cardIndex][1]):
            cards.append(lines[cardIndex + 1 + i])
    return totalNbCards


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    result = [part1(line.strip()) for line in lines]
    print("part1: ", sum([value[0] for value in result]))
    print("part2: ", part2(lines, result))
