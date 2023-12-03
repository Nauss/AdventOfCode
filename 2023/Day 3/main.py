from pathlib import Path
import re
import math

notSymbol = re.compile(r"\d|\.")
number = re.compile(r"(\d+)")


def convert(grid):
    result = [["0" for i in range(len(grid))] for j in range(len(grid[0]))]
    for i in range(len(result)):
        for j in range(len(result[i])):
            if notSymbol.match(grid[i][j]) is None:
                extendOne(result, i, j, "1")
    return result


def extendOne(grid, i, j, replacement):
    grid[i][j] = replacement
    if i > 0 and j > 0:
        grid[i - 1][j - 1] = replacement
    if i > 0:
        grid[i - 1][j] = replacement
    if i > 0 and j < len(grid[i]) - 1:
        grid[i - 1][j + 1] = replacement
    if j > 0:
        grid[i][j - 1] = replacement
    if j < len(grid[i]) - 1:
        grid[i][j + 1] = replacement
    if i < len(grid) - 1 and j > 0:
        grid[i + 1][j - 1] = replacement
    if i < len(grid) - 1:
        grid[i + 1][j] = replacement
    if i < len(grid) - 1 and j < len(grid[i]) - 1:
        grid[i + 1][j + 1] = replacement


def part1(grid):
    sum = 0
    checker = convert(grid)
    for i, line in enumerate(grid):
        for m in number.finditer("".join(line)):
            if checker[i][m.start()] != "0" or checker[i][m.end() - 1] != "0":
                sum += int(m.group())

    return sum


star = re.compile(r"\*")


def convertStar(grid):
    result = [["0" for i in range(len(grid))] for j in range(len(grid[0]))]
    for i in range(len(result)):
        for j in range(len(result[i])):
            if grid[i][j] == "*":
                extendOne(result, i, j, "✿")
                result[i][j] = "*"
    return result


def findClosestStar(checker, row, col):
    for i in range(row - 1, row + 2):
        if i < 0 or i >= len(checker):
            continue
        for j in range(col - 1, col + 2):
            if j < 0 or j >= len(checker[i]):
                continue
            if checker[i][j] == "*":
                return (i, j)


def part2(grid):
    gears = {}
    checker = convertStar(grid)
    for i, line in enumerate(grid):
        for m in number.finditer("".join(line)):
            starPosition = None
            if checker[i][m.start()] == "✿":
                starPosition = findClosestStar(checker, i, m.start())
            elif m.start() != m.end() and checker[i][m.end() - 1] == "✿":
                starPosition = findClosestStar(checker, i, m.end() - 1)
            if starPosition is not None:
                if starPosition not in gears:
                    gears[starPosition] = []
                gears[starPosition].append(int(m.group()))

    sum = 0
    for gear in gears:
        if len(gears[gear]) == 2:
            sum += math.prod(gears[gear])
    return sum


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    grid = []
    for line in lines:
        grid.append([*(line.strip())])
    print("part1: ", part1(grid))
    print("part2: ", part2(grid))
