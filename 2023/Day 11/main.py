from pathlib import Path
import numpy as np


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_range(a, b):
    return range(min(a[0], b[0]), max(a[0], b[0])), range(
        min(a[1], b[1]), max(a[1], b[1])
    )


def compute(grid, expand_factor):
    epmty_rows = []
    for i in range(len(grid)):
        if grid[i].count("#") == 0:
            epmty_rows.append(i)
    empty_cols = []
    for i in range(len(grid[0])):
        col = [grid[j][i] for j in range(len(grid))]
        if col.count("#") == 0:
            empty_cols.append(i)

    galaxies = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                galaxies.append((i, j))

    result = 0
    for galaxy1 in galaxies:
        for galaxy2 in galaxies:
            if galaxy1 == galaxy2:
                continue
            result += distance(galaxy1, galaxy2)
            ditance_range = get_range(galaxy1, galaxy2)
            for row in epmty_rows:
                if row in ditance_range[0]:
                    result += expand_factor
            for col in empty_cols:
                if col in ditance_range[1]:
                    result += expand_factor
    return result / 2


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [[c for c in line.strip()] for line in f.readlines()]
    result = compute(grid, 1)
    print("part1: ", result)
    result = compute(grid, 1000000 - 1)
    print("part2: ", result)
