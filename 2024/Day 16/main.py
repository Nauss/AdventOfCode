from pathlib import Path
import time

seatPositions = set()
cache = {}


# def reconstructPath(visited):
#     global seatPositions
#     for node in visited:
#         seatPositions.add(node)
def reconstructPath(current):
    global seatPositions
    seatPositions.add(current[0])
    if not current[3]:
        return
    for node in current[3]:
        reconstructPath(node)


def heuristic(position, endPos):
    distanceX = abs(position[0] - endPos[0])
    distanceY = abs(position[1] - endPos[1])
    return distanceX + distanceY + 1000


def rotation(current, direction):
    if direction == (0, -1):
        if current[1] == "N":
            return ("N", 0)
        elif current[1] == "E":
            return ("N", 1000)
        elif current[1] == "S":
            return ("N", 0)
        elif current[1] == "W":
            return ("N", 1000)
    elif direction == (0, 1):
        if current[1] == "N":
            return ("S", 0)
        elif current[1] == "E":
            return ("S", 1000)
        elif current[1] == "S":
            return ("S", 0)
        elif current[1] == "W":
            return ("S", 1000)
    elif direction == (-1, 0):
        if current[1] == "N":
            return ("W", 1000)
        elif current[1] == "E":
            return ("W", 0)
        elif current[1] == "S":
            return ("W", 1000)
        elif current[1] == "W":
            return ("W", 0)
    elif direction == (1, 0):
        if current[1] == "N":
            return ("E", 1000)
        elif current[1] == "E":
            return ("E", 0)
        elif current[1] == "S":
            return ("E", 1000)
        elif current[1] == "W":
            return ("E", 0)


def isVisited(visited, next):
    position, orientation, cost, previous = next
    for node in visited:
        if node[0] == position and node[1] == orientation and node[2] <= cost:
            return True
    return False


def findInList(visited, next):
    position, orientation, cost, previous = next
    for node in visited:
        if node[0] == position and node[1] == orientation and node[2] <= cost:
            return node
    return None


def part1(grid):
    startPos = None
    endPos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                startPos = (x, y)
            elif grid[y][x] == "E":
                endPos = (x, y)

    openList = [(startPos, "E", 0)]
    closedList = []
    shortest = 0
    while openList:
        openList.sort(key=lambda x: x[2])
        current = openList.pop(0)
        if current[0] == endPos:
            if shortest == 0 or current[2] < shortest:
                shortest = current[2]
        closedList.append(current)
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nextPos = (current[0][0] + direction[0], current[0][1] + direction[1])
            newOrientation, cost = rotation(current, direction)
            next = (nextPos, newOrientation, current[2] + 1 + cost)
            if grid[nextPos[1]][nextPos[0]] == "#":
                continue
            if isVisited(closedList, next):
                continue
            if isVisited(openList, next):
                continue
            openList.append(next)

    return shortest


def isNeighbour(pos1, pos2):
    return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1


def aStar(grid, startPos, direction, endPos):
    openList = [(startPos, direction, 0, None)]
    closedList = []
    while openList:
        openList.sort(key=lambda x: x[2])
        current = openList.pop(0)
        if current[0] == endPos:
            return current
        closedList.append(current)
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nextPos = (current[0][0] + direction[0], current[0][1] + direction[1])
            if current[3] and nextPos == current[3][0][0] or nextPos == startPos:
                continue
            newOrientation, cost = rotation(current, direction)
            next = (nextPos, newOrientation, current[2] + 1 + cost, [current])
            if grid[nextPos[1]][nextPos[0]] == "#":
                continue
            if isVisited(closedList, next):
                visited = findInList(closedList, next)
                if next[2] <= visited[2]:
                    visited[3].append(current)
                continue
            if isVisited(openList, next):
                visited = findInList(openList, next)
                if next[2] <= visited[2]:
                    visited[3].append(current)
                continue
            openList.append(next)


def getEmpty(grid, position):
    empty = []
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nextPos = (position[0] + direction[0], position[1] + direction[1])
        if grid[nextPos[1]][nextPos[0]] == "#":
            continue
        empty.append(nextPos)
    return empty


def opposite(direction):
    if direction == "N":
        return "S"
    elif direction == "S":
        return "N"
    elif direction == "E":
        return "W"
    elif direction == "W":
        return "E"


def part2(grid):
    startPos = None
    endPos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                startPos = (x, y)
            elif grid[y][x] == "E":
                endPos = (x, y)
    global seatPositions
    seatPositions.add(startPos)
    seatPositions.add(endPos)

    first = aStar(grid, startPos, "E", endPos)
    reconstructPath(first)

    return len(seatPositions)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    grid = lines
    for i in range(len(grid)):
        grid[i] = list(grid[i])
    result = part1(grid)
    print("part1: ", result)
    start = time.time()
    result = part2(lines)
    print("part2: ", result)
    print("Runtime: ", time.time() - start)
