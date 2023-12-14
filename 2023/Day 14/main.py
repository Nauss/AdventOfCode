import copy
from pathlib import Path
import time
import numpy as np


# def rotate(grid):
#     result = copy.deepcopy(grid)
#     result = np.rot90(grid, 1)
#     return result


# def tilt(grid):
#     result = copy.deepcopy(grid)
#     row_index = 0
#     while row_index < len(result):
#         row = result[row_index]
#         col_index = 1
#         moved = False
#         while col_index < len(row):
#             previous = row[col_index - 1]
#             current = row[col_index]
#             if previous == "." and current == "O":
#                 row[col_index - 1] = "O"
#                 row[col_index] = "."
#                 moved = True
#             col_index += 1
#         if not moved:
#             row_index += 1
#     return result


# def count(grid):
#     result = 0
#     for row in grid:
#         size = len(row)
#         for index, col in enumerate(row):
#             if col == "O":
#                 result += size - index
#     return result


# def part1(grid):
#     rotated = rotate(grid)
#     tilted = tilt(rotated)
#     return count(tilted)


def __repr__(self):
    s0, s1 = self.shape
    result = "\n"
    for row in self:
        result += "".join(row) + "\n"
    result += "\n"
    return result


np.set_string_function(__repr__)


def tilt(grid):
    row_index = 0
    while row_index < len(grid):
        row = grid[row_index]
        col_index = 1
        moved = False
        while col_index < len(row):
            previous = row[col_index - 1]
            current = row[col_index]
            if previous == "." and current == "O":
                row[col_index - 1] = "O"
                row[col_index] = "."
                moved = True
            col_index += 1
        if not moved:
            row_index += 1


def count(grid):
    result = 0
    for row in grid:
        size = len(row)
        for index, col in enumerate(row):
            if col == "O":
                result += size - index
    return result


def apply_cycle(grid, cycle):
    for _ in range(cycle):
        # north to the left
        grid = np.rot90(grid, 1)
        tilt(grid)
        # west to the left
        grid = np.rot90(grid, -1)
        tilt(grid)
        # south to the left
        grid = np.rot90(grid, -1)
        tilt(grid)
        # east to the left
        grid = np.rot90(grid, -1)
        tilt(grid)
        grid = np.rot90(grid, 2)


def detect_cycle(grids):
    for index, grid in enumerate(grids):
        if index < len(grids) - 1 and np.array_equal(grid, grids[-1]):
            return index
    return -1


def part2(grid):
    grids = [grid]
    index = -1
    while index == -1:
        grid_copy = copy.deepcopy(grids[-1])
        grids.append(grid_copy)
        apply_cycle(grid_copy, 1)
        index = detect_cycle(grids)

    nb_cycles = (1000000000 - index) % (len(grids) - index - 1)
    print(index, nb_cycles)
    grid_copy = copy.deepcopy(grids[-1])
    for _ in range(nb_cycles):
        apply_cycle(grid_copy, 1)
    return count(np.rot90(grid_copy, 1))


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = np.array([[c for c in line.strip()] for line in f.readlines()])
    # result = part1(grid)
    # print("part1: ", result)
    t = time.time()
    result = part2(grid)
    print(f"part2 {time.time() - t}: ", result)
