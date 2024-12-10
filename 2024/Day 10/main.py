from pathlib import Path
import time


def getNextStep(map, x, y):
    print(x, y)
    if x < 0 or y < 0 or x >= len(map[0]) or y >= len(map):
        return

    value = map[y][x] + 1
    positions = []
    if map[y - 1][x] == next:
        positions.append((x, y - 1))
    if map[y + 1][x] == next:
        positions.append((x, y + 1))
    if map[y][x - 1] == next:
        positions.append((x - 1, y))
    if map[y][x + 1] == next:
        positions.append((x + 1, y))

    return positions, value


def findTrails(map, x, y):
    result = 0
    positions, value = getNextStep(map, x, y)
    while len(positions):
        pos = positions.pop()
        if value == 9:
            result += 1
        newPositions, value = findTrails(map, pos[0], pos[1])
        positions.extend(newPositions)

    return result


def part1(map):
    print(map)
    result = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 0:
                result += findTrails(map, x, y)
    return result


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    map = [list(int(i) for i in line.strip()) for line in f]
    result = part1(map)
    print("part1: ", result)
    # start = time.time()
    # result = part2(diskMap)
    # print("part2: ", result)
    # print("Runtime: ", time.time() - start)
