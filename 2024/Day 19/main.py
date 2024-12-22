from pathlib import Path
import re


def getNextTowels(currents, towels, design):
    maxTowelsLen = max([len(x) for x in towels])
    nexts = set()
    maxLen = 0
    for current in currents:
        dIndex = current
        size = min(maxTowelsLen, len(design) - dIndex)
        while True:
            if size == 0:
                break
            if design[dIndex : dIndex + size] in towels:
                next = current + size
                if not design[0 : current + size] in towels:
                    towels.add(design[0 : current + size])
                if next > maxLen:
                    maxLen = next
                nexts.add(next)
            size -= 1
    return nexts, maxLen


def part1(towels, designs):
    possible = 0
    for design in designs:
        currents = set([0])
        while True:
            nexts, maxLen = getNextTowels(currents, towels, design)
            if len(nexts) == 0:
                break
            if maxLen == len(design):
                # Found
                possible += 1
                break
            currents = nexts
    return possible


def findNext(towels, cache, design):
    if design == "":
        return 1
    if design not in cache:
        result = 0
        for towel in towels:
            if design.startswith(towel):
                nextDesign = design[len(towel) :]
                result += findNext(towels, cache, nextDesign)
        cache[design] = result
    return cache[design]


def part2(towels, designs):
    cache = {}
    total = 0
    for design in designs:
        total += findNext(towels, cache, design)

    return total


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    towels = set(lines[0].split(", "))
    designs = lines[2:]
    result = part1(towels, designs)
    print("part1: ", result)
    # start = time.time()
    result = part2(towels, designs)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
