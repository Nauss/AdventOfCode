from collections import Counter
from pathlib import Path
import re
import math

maps_regex = re.compile(r"(.*) = \((.*), (.*)\)")


def part1(maps, directions):
    result = 0
    position = "AAA"
    direction_index = 0
    while True:
        if directions[direction_index] == "L":
            position = maps[position][0]
        else:
            position = maps[position][1]
        direction_index += 1
        result += 1
        if direction_index == len(directions):
            direction_index = 0
        if position == "ZZZ":
            break

    return result


def part2(maps, directions):
    positions_period = []
    positions = [pos for pos in maps.keys() if pos[2] == "A"]
    for position in positions:
        direction_index = 0
        period = 0
        while True:
            if directions[direction_index] == "L":
                position = maps[position][0]
            else:
                position = maps[position][1]
            direction_index += 1
            period += 1
            if direction_index == len(directions):
                direction_index = 0
            if position[2] == "Z":
                break
        positions_period.append(period)

    return math.lcm(*positions_period)


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    directions = list(f.readline().strip())
    f.readline()
    lines = f.readlines()
    maps = {}
    for line in lines:
        line = maps_regex.match(line.strip()).groups()
        maps[line[0]] = (line[1], line[2])
    result = part1(maps, directions)
    is_part2 = True
    print("part1: ", result)
    result = part2(maps, directions)
    print("part2: ", result)
