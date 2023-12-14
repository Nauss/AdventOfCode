import copy
from pathlib import Path
import numpy as np

def rotate(grid, direction):
    result = copy.deepcopy(grid)
    if direction == 'north':
        result = np.rot90(grid, 1)
    return result

def tilt(grid):
    result = copy.deepcopy(grid)
    row_index = 0
    while row_index < len(result):
        row = result[row_index]
        col_index = 1
        moved = False
        while col_index < len(row):
            previous = row[col_index - 1]
            current = row[col_index]
            if previous == '.' and current == 'O':
                row[col_index - 1] = 'O'
                row[col_index] = '.'
                moved = True
            col_index += 1
        if not moved:
            row_index += 1
    return result

def count(grid):
    result = 0
    for row in grid:
        size = len(row)
        for index, col  in enumerate(row):
            if col == 'O':
                result += size - index
    return result

def compute(grid):
    result = 0
    rotated = rotate(grid, 'north')
    tilted = tilt(rotated)
    print(repr(tilted))
    return count(tilted)

path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = np.array([[c for c in line.strip()] for line in f.readlines()])
    print(repr(grid))
    result = compute(grid)
    print("part1: ", result)
    # result = compute(grid, 1000000 - 1)
    # print("part2: ", result)
