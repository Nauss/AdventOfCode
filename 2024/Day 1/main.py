from pathlib import Path
import re


def part1(lines):
    list1 = [int(x[0]) for x in lines]
    list2 = [int(x[1]) for x in lines]
    list1.sort()
    list2.sort()
    diff = [abs(list2[i] - list1[i]) for i in range(len(list1))]
    return sum(diff)


def part2(line):
    list1 = [int(x[0]) for x in lines]
    list2 = [int(x[1]) for x in lines]
    similarity = [x * list2.count(x) for x in list1]
    return sum(similarity)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split() for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
