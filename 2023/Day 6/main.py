from pathlib import Path
import math


def compute(times, distances):
    records = []
    for index, time in enumerate(times):
        distance = distances[index]
        break_record = 0
        for t in range(1, time - 1):
            if t * (time - t) > distance:
                break_record += 1
        records.append(break_record)
    return math.prod(records)


# Open data.txt file
times = [56, 71, 79, 99]
distances = [334, 1135, 1350, 2430]
print("part1: ", compute(times, distances))
times = [56717999]
distances = [334113513502430]
print("part2: ", compute(times, distances))
