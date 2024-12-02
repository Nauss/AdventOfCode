from pathlib import Path

maxLevelDiff = 3


def isSafe(line, remove=False):
    global nbFixed
    order = None
    for i in range(len(line) - 1):
        diff = line[i + 1] - line[i]
        if order is None:
            order = "asc" if diff > 0 else "desc"
        if (
            diff == 0
            or abs(diff) > maxLevelDiff
            or (order == "asc" and diff < 0)
            or (order == "desc" and diff > 0)
        ):
            if remove:
                for j in range(len(line)):
                    copy = line.copy()
                    del copy[j]
                    if isSafe(copy):
                        return True
            return False
    return True


def part1(lines):
    nbSafe = 0
    for line in lines:
        if isSafe(line):
            nbSafe += 1
    return nbSafe


def part2(lines):
    nbSafe = 0
    for line in lines:
        if isSafe(line, True):
            nbSafe += 1
    return nbSafe


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [[int(x) for x in line.strip().split()] for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
