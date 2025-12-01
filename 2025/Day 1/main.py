from pathlib import Path


def part1(lines):
    numbers = [int(x.replace("L", "-").replace("R", "+")) for x in lines]
    dial = 50
    count = 0
    for x in numbers:
        dial += x
        dial = dial % 100
        if dial == 0:
            count += 1

    return count


def part2(lines):
    numbers = [int(x.replace("L", "-").replace("R", "+")) for x in lines]
    dial = 50
    count = 0
    for x in numbers:
        diff = 1 if x > 0 else -1
        for i in range(0, abs(x)):
            dial += diff
            if dial < 0:
                dial = 99
            if dial > 99:
                dial = 0
            if dial == 0:
                count += 1

    return count


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
