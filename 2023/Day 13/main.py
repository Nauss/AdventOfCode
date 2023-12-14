import copy
from pathlib import Path

import numpy as np


def convert_to_grids(lines):
    grids = []
    grid = []
    for line in lines:
        if len(line) == 0:
            grids.append(np.array((grid)))
            grid = []
        else:
            grid.append(line)

    grids.append(np.array((grid)))
    return grids


def fix(grid, before, after):
    size = len(grid[0, :])
    for i in range(size):
        if before[i] != after[i]:
            before[i] = after[i]
            break


def check(grid, fix_smudge=False):
    previous = grid[0, :].copy()
    size = len(grid[:, 0])
    temporary_result = None
    for i in range(1, size):
        corrected = False
        if np.array_equal(grid[i, :], previous):
            perfect_symetry = True
            for j in range(i):
                if i - 2 - j < 0 or i + 1 + j >= size:
                    if fix_smudge:
                        if temporary_result is None and corrected:
                            temporary_result = (i, corrected)
                        perfect_symetry = False
                        corrected = False
                    break
                before = grid[i - 2 - j, :].copy()
                after = grid[i + 1 + j, :]
                if not np.array_equal(before, after):
                    perfect_symetry = False
                    if fix_smudge:
                        perfect_symetry = True
                        fix(grid, before, after)
                        if not np.array_equal(before, after):
                            perfect_symetry = False
                            break
                        else:
                            corrected = True
            if perfect_symetry:
                return (i, corrected)
        elif fix_smudge:
            perfect_symetry = True
            fix(grid, previous, grid[i, :])
            if not np.array_equal(previous, grid[i, :]):
                perfect_symetry = False
                # break
            else:
                corrected = True
                for j in range(i):
                    if i - 2 - j < 0 or i + 1 + j >= size:
                        if fix_smudge:
                            if temporary_result is None and corrected:
                                temporary_result = (i, corrected)
                            perfect_symetry = False
                            corrected = False
                        break
                    before = grid[i - 2 - j, :].copy()
                    after = grid[i + 1 + j, :]
                    if not np.array_equal(before, after):
                        perfect_symetry = False
                        corrected = False
                if perfect_symetry:
                    return (i, corrected)
        previous = grid[i, :].copy()
    return temporary_result


# def part1(grids):
#     result = 0
#     for grid in grids:
#         vertical = check_vertical(grid)
#         if vertical is not None:
#             result += vertical
#         horizontal = check_horizontal(grid)
#         if horizontal is not None:
#             result += 100 * horizontal
#     return result


def part2(grids):
    result = 0
    for grid in grids:
        check_result = check(grid, True)
        if check_result is not None and not check_result[0] is None and check_result[1]:
            result += 100 * check_result[0]
        rotated = np.rot90(copy.deepcopy(grid), axes=(1, 0))
        check_result = check(rotated, True)
        if check_result is not None and not check_result[0] is None and check_result[1]:
            result += check_result[0]
    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [list(line.strip()) for line in f.readlines()]
    grids = convert_to_grids(lines)
    # result = part1(grids)
    # print("part1: ", result)
    result = part2(grids)
    print("part2: ", result)
