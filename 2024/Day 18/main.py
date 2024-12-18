from pathlib import Path
import time


def isVisited(visited, next):
    position, cost = next
    for node in visited:
        if node[0] == position and node[1] <= cost:
            return True
    return False


def aStar(grid):
    openList = [((0, 0), 0)]
    closedList = []
    while openList:
        openList.sort(key=lambda x: x[1])
        current = openList.pop(0)
        if current[0] == (70, 70):
            return current
        closedList.append(current)
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nextPos = (current[0][0] + direction[0], current[0][1] + direction[1])
            if nextPos[0] < 0 or nextPos[0] >= 71 or nextPos[1] < 0 or nextPos[1] >= 71:
                continue
            next = (nextPos, current[1] + 1)
            if grid[nextPos[1]][nextPos[0]] == "#":
                continue
            if isVisited(closedList, next):
                continue
            if isVisited(openList, next):
                continue
            openList.append(next)
    return current


def part1(grid):
    return aStar(grid)[1]


def part2(grid, positions):
    bytesFallen = 1024
    while True:
        position = positions[bytesFallen]
        grid[position[1]][position[0]] = "#"
        current = aStar(grid)
        if current[0] != (70, 70):
            return position

        bytesFallen += 1


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    positions = []
    grid = [["." for _ in range(71)] for _ in range(71)]
    bytesFallen = 0
    for line in lines:
        x, y = line.split(",")
        position = (int(x), int(y))
        positions.append(position)
        if bytesFallen < 1024:
            grid[position[1]][position[0]] = "#"
        bytesFallen += 1
    result = part1(grid)
    print("part1: ", result)
    # start = time.time()
    result = part2(grid, positions)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
