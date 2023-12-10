from pathlib import Path
import numpy as np


def next_position(grid, previous, position):
    row, col = position
    if grid[row][col] == "|":
        result = (row - 1, col)
        if result == previous:
            result = (row + 1, col)
        return result
    elif grid[row][col] == "-":
        result = (row, col - 1)
        if result == previous:
            result = (row, col + 1)
        return result
    elif grid[row][col] == "L":
        result = (row, col + 1)
        if result == previous:
            result = (row - 1, col)
        return result
    elif grid[row][col] == "J":
        result = (row, col - 1)
        if result == previous:
            result = (row - 1, col)
        return result
    elif grid[row][col] == "7":
        result = (row, col - 1)
        if result == previous:
            result = (row + 1, col)
        return result
    elif grid[row][col] == "F":
        result = (row + 1, col)
        if result == previous:
            result = (row, col + 1)
        return result


def next_positions(grid, previous, position):
    return (
        next_position(grid, previous[0], position[0]),
        next_position(grid, previous[1], position[1]),
    )


def part1(grid):
    distance = 0
    distances = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    start = (102, 118)  # 7
    currrent = (start, start)
    previous = ((102, 117), (103, 118))
    while True:
        next = next_positions(grid, previous, currrent)
        previous = currrent
        currrent = next
        p1 = currrent[0]
        p2 = currrent[1]
        if p1 == start or p2 == start:
            break
        distance += 1
        if distances[p1[0]][p1[1]] == 0:
            distances[p1[0]][p1[1]] = distance
        if distances[p2[0]][p2[1]] == 0:
            distances[p2[0]][p2[1]] = distance

    return np.amax(distances)


def is_inside(distances, row, col):
    if distances[row][col] != 0:
        # On the loop
        return False
    index = 1
    crossings = 0
    direction = 0
    current_distance = 0
    line = False
    while True:
        if col + index >= len(distances[0]):
            break
        distance = distances[row][col + index]
        if distance != 0:
            if not line and abs(current_distance - distance) == 1:
                line = True
            if row - 1 >= 0 and (
                abs(distances[row - 1][col + index] - distance) == 1
                or distances[row - 1][col + index] == 1
            ):
                if line:
                    if direction != 1:
                        crossings += 1
                    line = False
                    direction = 0
                else:
                    direction = -1
                    crossings += 1
            elif row + 1 < len(distances) and (
                abs(distances[row + 1][col + index] - distance) == 1
                or distances[row + 1][col + index] == 1
            ):
                if line:
                    if direction != -1:
                        crossings += 1
                    line = False
                    direction = 0
                else:
                    direction = 1
                    crossings += 1

            current_distance = distance
        index += 1

    return crossings % 2 == 1


def part2(distances):
    distance = 0
    distances = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    start = (102, 118)  # 7
    currrent = start
    previous = (102, 117)
    while True:
        next = next_position(grid, previous, currrent)
        previous = currrent
        currrent = next
        if currrent == start:
            break
        distance += 1
        if distances[currrent[0]][currrent[1]] == 0:
            distances[currrent[0]][currrent[1]] = distance
    distance += 1
    distances[start[0]][start[1]] = distance

    result = 0
    for row in range(len(distances)):
        for col in range(len(distances[0])):
            if is_inside(distances, row, col):
                result += 1
    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [[c for c in line.strip()] for line in f.readlines()]
    result = part1(grid)
    print("part1: ", result)
    result = part2(grid)
    print("part2: ", result)
