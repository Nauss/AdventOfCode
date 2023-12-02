from pathlib import Path
import re
import math

gameRegex = re.compile(r"Game (\d+): (.*)$")
colorRegex = re.compile(r"(\d+) (.*)")
limits = {"red": 12, "green": 13, "blue": 14}


def part1(line):
    match = gameRegex.search(line)
    for color in match[2].replace(";", ",").split(", "):
        colorMatch = colorRegex.search(color)
        if int(colorMatch[1]) > limits[colorMatch[2]]:
            return 0

    return int(match[1])


def part2(line):
    match = gameRegex.search(line)
    minimas = {"red": 0, "green": 0, "blue": 0}
    for color in match[2].replace(";", ",").split(", "):
        colorMatch = colorRegex.search(color)
        value = int(colorMatch[1])
        color = colorMatch[2]
        if value > minimas[color]:
            minimas[color] = value

    return minimas["red"] * minimas["green"] * minimas["blue"]


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    result = [part1(line) for line in lines]
    print("part1: ", sum(result))
    result = [part2(line) for line in lines]
    print("part2: ", sum(result))
