from pathlib import Path
import re


def getTowels(current, design, towels):

    return result


def getNextTowels(currents, towels, design):
    nexts = []
    for current in currents:
        dIndex = len(current)
        size = 1
        while True:
            if dIndex + size > len(design):
                break
            if design[dIndex : dIndex + size] in towels:
                nexts.append(current + design[dIndex : dIndex + size])
            size += 1
    return nexts


def part1(towels, designs):
    impossible = 0
    for design in designs:
        currents = [""]
        while True:
            nexts = getNextTowels(currents, towels, design)
            if len(nexts) == 0:
                impossible += 1
                break
            if max([len(x) for x in nexts]) == len(design):
                # Found
                break
            currents = nexts
    return len(designs) - impossible


def part2(line):
    list1 = [int(x[0]) for x in lines]
    list2 = [int(x[1]) for x in lines]
    similarity = [x * list2.count(x) for x in list1]
    return sum(similarity)


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
    # result = part2(lines)
    # print("part2: ", result)
    # print("Runtime: ", time.time() - start)
