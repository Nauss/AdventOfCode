from pathlib import Path
import time


def countNeighbours(grid, x, y, plant):
    sizeX = len(grid[0])
    sizeY = len(grid)
    count = 0
    if x > 0 and grid[y][x - 1] == plant:
        count += 1
    if x < sizeX - 1 and grid[y][x + 1] == plant:
        count += 1
    if y > 0 and grid[y - 1][x] == plant:
        count += 1
    if y < sizeY - 1 and grid[y + 1][x] == plant:
        count += 1
    return count


def computePrice(grid, x, y, visited):
    sizeX = len(grid[0])
    sizeY = len(grid)
    stack = [(x, y)]
    plant = grid[y][x]
    area = 0
    perimeter = 0
    while len(stack):
        x, y = stack.pop()
        if x < 0 or x >= sizeX or y < 0 or y >= sizeY:
            continue
        if grid[y][x] != plant:
            continue
        if (x, y) in visited:
            continue
        visited.add((x, y))
        area += 1
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
        perimeter += 4 - countNeighbours(grid, x, y, plant)
    return perimeter * area


def part1(grid):
    visited = set()
    sizeX = len(grid[0])
    sizeY = len(grid)
    totalPrice = 0
    for y in range(sizeY):
        for x in range(sizeX):
            if (x, y) in visited:
                continue
            totalPrice += computePrice(grid, x, y, visited)
    return totalPrice


def isSame(grid, x, y, plant):
    sizeX = len(grid[0])
    sizeY = len(grid)
    if x < 0 or x >= sizeX or y < 0 or y >= sizeY:
        return False
    return grid[y][x] == plant


def addCorner(corners, x, y):
    if (x, y) not in corners:
        corners[(x, y)] = 0
    corners[(x, y)] += 1


def sameRegion(grid, x1, y1, x2, y2):
    sizeX = len(grid[0])
    sizeY = len(grid)
    stack = [(x1, y1)]
    plant = grid[y1][x1]
    visited = set()
    while len(stack):
        x, y = stack.pop()
        if x < 0 or x >= sizeX or y < 0 or y >= sizeY:
            continue
        if grid[y][x] != plant:
            continue
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) == (x2, y2):
            return True
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
    return False


def updateCorners(corners, grid, x, y):
    sizeX = len(grid[0])
    sizeY = len(grid)
    plant = grid[y][x]
    # if (isSame(grid, x - 1, y, plant) and isSame(grid, x + 1, y, plant)) and (
    #     isSame(grid, x, y - 1, plant) or isSame(grid, x, y + 1, plant)
    # ):
    #     return
    # if (isSame(grid, x, y - 1, plant) and isSame(grid, x, y + 1, plant)) and (
    #     isSame(grid, x - 1, y, plant) or isSame(grid, x + 1, y, plant)
    # ):
    #     return
    if x == 0 and y == 0:
        addCorner(corners, x - 0.5, y - 0.5)
    if x == sizeX - 1 and y == 0:
        addCorner(corners, x + 0.5, y - 0.5)
    if x == 0 and y == sizeY - 1:
        addCorner(corners, x - 0.5, y + 0.5)
    if x == sizeX - 1 and y == sizeY - 1:
        addCorner(corners, x + 0.5, y + 0.5)

    # Top Left
    if (
        isSame(grid, x - 1, y, plant)
        and isSame(grid, x, y - 1, plant)
        and not isSame(grid, x - 1, y - 1, plant)
    ):
        addCorner(corners, x - 0.5, y - 0.5)
    if not isSame(grid, x - 1, y, plant) and not isSame(grid, x, y - 1, plant):
        addCorner(corners, x - 0.5, y - 0.5)

    # Top Right
    if (
        isSame(grid, x + 1, y, plant)
        and isSame(grid, x, y - 1, plant)
        and not isSame(grid, x + 1, y - 1, plant)
    ):
        addCorner(corners, x + 0.5, y - 0.5)
    if not isSame(grid, x + 1, y, plant) and not isSame(grid, x, y - 1, plant):
        addCorner(corners, x + 0.5, y - 0.5)

    # Bottom Left
    if (
        isSame(grid, x - 1, y, plant)
        and isSame(grid, x, y + 1, plant)
        and not isSame(grid, x - 1, y + 1, plant)
    ):
        addCorner(corners, x - 0.5, y + 0.5)
    if not isSame(grid, x - 1, y, plant) and not isSame(grid, x, y + 1, plant):
        addCorner(corners, x - 0.5, y + 0.5)
        if isSame(grid, x - 1, y + 1, plant) and sameRegion(grid, x, y, x - 1, y + 1):
            addCorner(corners, x - 0.6, y + 0.6)

    # Bottom Right
    if (
        isSame(grid, x + 1, y, plant)
        and isSame(grid, x, y + 1, plant)
        and not isSame(grid, x + 1, y + 1, plant)
    ):
        addCorner(corners, x + 0.5, y + 0.5)
    if not isSame(grid, x + 1, y, plant) and not isSame(grid, x, y + 1, plant):
        addCorner(corners, x + 0.5, y + 0.5)
        if isSame(grid, x + 1, y + 1, plant) and sameRegion(grid, x, y, x + 1, y + 1):
            addCorner(corners, x + 0.6, y + 0.6)


def computePrice2(grid, x, y, visited):
    sizeX = len(grid[0])
    sizeY = len(grid)
    stack = [(x, y)]
    plant = grid[y][x]
    area = 0
    corners = {}
    while len(stack):
        x, y = stack.pop()
        if x < 0 or x >= sizeX or y < 0 or y >= sizeY:
            continue
        if grid[y][x] != plant:
            continue
        if (x, y) in visited:
            continue
        visited.add((x, y))
        area += 1
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
        updateCorners(corners, grid, x, y)

    return area * len(corners)


def part2(grid):
    visited = set()
    sizeX = len(grid[0])
    sizeY = len(grid)
    totalPrice = 0
    for y in range(sizeY):
        for x in range(sizeX):
            if (x, y) in visited:
                continue
            totalPrice += computePrice2(grid, x, y, visited)
    return totalPrice


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [line.strip() for line in f]
    result = part1(grid)
    print("part1: ", result)
    # start = time.time()
    result = part2(grid)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
