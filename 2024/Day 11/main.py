from pathlib import Path
import time
import functools


def applyRules(value):
    strValue = str(value)
    if value == 0:
        return [1]
    if len(strValue) % 2 == 0:
        return [
            int(strValue[: len(strValue) // 2]),
            int(strValue[len(strValue) // 2 :]),
        ]
    else:
        return [value * 2024]


def getCache(value, cache, blinks):
    if (value, blinks) in cache:
        return cache[(value, blinks)]
    if blinks == 0:
        return 1

    applied = applyRules(value)
    cache[(value, blinks)] = getCache(applied[0], cache, blinks - 1)
    if len(applied) > 1:
        cache[(value, blinks)] += getCache(applied[1], cache, blinks - 1)
    return cache[(value, blinks)]


def solve(line, cache, blinks):
    nbStones = 0
    for i in range(len(line)):
        nbStones += getCache(line[i], cache, blinks)

    return nbStones


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    line = [int(x) for x in [line.strip().split(" ") for line in f][0]]
    cache = {}
    result = solve(line, cache, 25)
    print("part1: ", result)
    start = time.time()
    result = solve(line, cache, 75)
    print("part2: ", result)
    print("Runtime: ", time.time() - start)


# @functools.lru_cache(maxsize=None)
# def getCache(value, blinks):
#     if blinks == 0:
#         return 1

#     applied = applyRules(value)
#     result = getCache(applied[0], blinks - 1)
#     if len(applied) > 1:
#         result += getCache(applied[1], blinks - 1)
#     return result


# def solve(line, blinks):
#     nbStones = 0
#     for i in range(len(line)):
#         nbStones += getCache(line[i], blinks)

#     return nbStones


# # Open data.txt file
# path = Path(__file__).parent / "./data.txt"
# with path.open() as f:
#     # Read all lines
#     line = [int(x) for x in [line.strip().split(" ") for line in f][0]]
#     result = solve(line, 25)
#     print("part1: ", result)
#     start = time.time()
#     result = solve(line, 75)
#     print("part2: ", result)
#     print("Runtime: ", time.time() - start)
