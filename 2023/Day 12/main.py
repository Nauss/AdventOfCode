import functools
from pathlib import Path
import time

import numpy as np

# Inspiration from https://www.reddit.com/r/adventofcode/comments/18hg99r/2023_day_12_simple_tutorial_with_memoization/


@functools.lru_cache(maxsize=None)
def solve(springs, groups, i):
    if len(groups) == 0:
        while i < len(springs):
            if springs[i] == "#":
                #  No more groups but still a spring, no solution
                return 0
            i += 1
        #  No more groups, one solution found
        return 1

    #  Skip '.'
    while i < len(springs) and springs[i] == ".":
        i += 1

    result = 0
    if i >= len(springs):
        #  No more springs, no solution
        return 0

    # Check if the first group fits
    fits = True
    for j in range(groups[0]):
        if i + j >= len(springs) or springs[i + j] == ".":
            fits = False
            break

    if fits and ((i + j + 1) >= len(springs) or springs[i + j + 1] != "#"):
        # First group found, continue with the next one
        result += solve(springs, groups[1:], i + groups[0] + 1)

    # Try the other solution if we are on a '?'
    if springs[i] == "?":
        #  It becomes a '.' we skip it
        result += solve(springs, groups, i + 1)

    return result


def compute(lines):
    results = []
    for line in lines:
        result = solve(line[0], line[1], 0)
        results.append(result)
    return sum(results)


def expand_line(line):
    result_array = np.repeat("".join(line[0]), 5)
    springs = tuple("?".join(result_array))
    groups = []
    for i in range(5):
        groups += line[1]
    return (springs, tuple(groups))


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split(" ") for line in f.readlines()]
    lines = [
        (tuple(line[0]), tuple([int(c) for c in line[1].split(",")])) for line in lines
    ]
    print("part1: ", compute(lines))
    t = time.time()
    expanded_lines = [expand_line(line) for line in lines]
    result = compute(expanded_lines)
    print(f"part2 {time.time() - t}: ", result)
