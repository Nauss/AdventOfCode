from pathlib import Path
import time


def getNextStep(map, x, y):
    sizeX = len(map[0])
    sizeY = len(map)

    value = map[y][x] - 1
    positions = []
    if y > 0 and map[y - 1][x] == value:
        positions.append((x, y - 1))
    if y < sizeY - 1 and map[y + 1][x] == value:
        positions.append((x, y + 1))
    if x > 0 and map[y][x - 1] == value:
        positions.append((x - 1, y))
    if x < sizeX - 1 and map[y][x + 1] == value:
        positions.append((x + 1, y))

    return positions


def findTrails(result, visited, map, x, y):
    positions = getNextStep(map, x, y)
    while len(positions):
        pos = positions.pop()
        if pos in visited:
            continue
        visited[pos] = True
        if map[pos[1]][pos[0]] == 0:
            if pos not in result:
                result[pos] = 0
            result[pos] += 1
        else:
            findTrails(result, visited, map, pos[0], pos[1])


def part1(map):
    result = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 9:
                visited = {}
                findTrails(result, visited, map, x, y)
    return sum(result.values())


def findTrails2(result, visited, map, x, y):
    positions = getNextStep(map, x, y)
    while len(positions):
        pos = positions.pop()
        visited[pos] = True
        if map[pos[1]][pos[0]] == 0:
            if pos in visited:
                if pos not in result:
                    result[pos] = 0
                result[pos] += 1
        else:
            findTrails2(result, visited, map, pos[0], pos[1])


def part2(map):
    result = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 9:
                visited = {}
                findTrails2(result, visited, map, x, y)
    return sum(result.values())


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    map = [list(int(i) for i in line.strip()) for line in f]
    result = part1(map)
    print("part1: ", result)
    # start = time.time()
    result = part2(map)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
