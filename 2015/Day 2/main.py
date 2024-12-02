from pathlib import Path


def part1(lines):
    surface = 0
    for l, w, h in lines:
        sides = [l * w, w * h, h * l]
        surface += 2 * sum(sides) + min(sides)
    return surface


def part2(lines):
    ribbon = 0
    for l, w, h in lines:
        sides = sorted([l, w, h])
        ribbon += 2 * sum(sides[0:2]) + l * w * h
    return ribbon


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split("x") for line in f.readlines()]
    lines = [(int(l), int(w), int(h)) for [l, w, h] in lines]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
