from pathlib import Path
import time
import copy


def move(grid, position, direction):
    nextPosition = position
    if direction == "^":
        nextPosition = (position[0], position[1] - 1)
    elif direction == "v":
        nextPosition = (position[0], position[1] + 1)
    elif direction == "<":
        nextPosition = (position[0] - 1, position[1])
    elif direction == ">":
        nextPosition = (position[0] + 1, position[1])

    next = grid[nextPosition[1]][nextPosition[0]]
    if next == "#":
        return None
    elif next == ".":
        tmp = grid[position[1]][position[0]]
        grid[position[1]][position[0]] = "."
        grid[nextPosition[1]][nextPosition[0]] = tmp
        return nextPosition
    else:
        if move(grid, nextPosition, direction):
            tmp = grid[position[1]][position[0]]
            grid[position[1]][position[0]] = "."
            grid[nextPosition[1]][nextPosition[0]] = tmp
            return nextPosition
    return None


def countBoxes(grid):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                count += 100 * y + x
    return count


def part1(grid, directions):
    size = len(grid)
    position = (size // 2 - 1, size // 2 - 1)
    for direction in directions:
        nextPosition = move(grid, position, direction)
        if nextPosition:
            position = nextPosition

    return countBoxes(grid)


grid = []


def move2(position, direction):
    global grid
    gridCopy = copy.deepcopy(grid)
    nextPosition = position
    if direction == "^":
        nextPosition = (position[0], position[1] - 1)
    elif direction == "v":
        nextPosition = (position[0], position[1] + 1)
    elif direction == "<":
        nextPosition = (position[0] - 1, position[1])
    elif direction == ">":
        nextPosition = (position[0] + 1, position[1])

    next = grid[nextPosition[1]][nextPosition[0]]
    if next == "#":
        return None
    elif next == ".":
        tmp = grid[position[1]][position[0]]
        grid[position[1]][position[0]] = "."
        grid[nextPosition[1]][nextPosition[0]] = tmp
        return nextPosition
    else:
        if direction in ["^", "v"]:
            if next == "[":
                otherPosition = move2((nextPosition[0] + 1, nextPosition[1]), direction)
                if not otherPosition:
                    grid = gridCopy
                    return None
                # else:
                #     tmp = grid[position[1]][position[0] + 1]
                #     grid[position[1]][position[0] + 1] = "."
                #     grid[otherPosition[1]][otherPosition[0]] = tmp
            elif next == "]":
                otherPosition = move2((nextPosition[0] - 1, nextPosition[1]), direction)
                if not otherPosition:
                    grid = gridCopy
                    return None
                # else:
                #     tmp = grid[position[1]][position[0] + 1]
                #     grid[position[1]][position[0] + 1] = "."
                #     grid[otherPosition[1]][otherPosition[0]] = tmp
        if move2(nextPosition, direction):
            tmp = grid[position[1]][position[0]]
            grid[position[1]][position[0]] = "."
            grid[nextPosition[1]][nextPosition[0]] = tmp
            return nextPosition
        if direction in ["^", "v"]:
            grid = gridCopy
    return None


def countBoxes2(grid):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "[":
                count += 100 * y + x
    return count


def part2(directions):
    global grid
    newGrid = []
    for y in range(len(grid)):
        newGrid.append([])
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                newGrid[y].append(grid[y][x])
                newGrid[y].append("#")
            if grid[y][x] == "O":
                newGrid[y].append("[")
                newGrid[y].append("]")
            if grid[y][x] == ".":
                newGrid[y].append(grid[y][x])
                newGrid[y].append(".")
            if grid[y][x] == "@":
                newGrid[y].append(grid[y][x])
                newGrid[y].append(".")
    grid = newGrid
    size = len(grid)
    # position = (10, 3)
    position = (size - 2, size // 2 - 1)
    for direction in directions:
        if direction == "v" and position[0] == 11 and position[1] == 3:
            pass
        nextPosition = move2(position, direction)
        if nextPosition:
            position = nextPosition

    return countBoxes2(grid)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    size = lines.index("")
    # grid = lines[:size]
    # for i in range(size):
    #     grid[i] = list(grid[i])
    # print(grid)
    # result = part1(grid, "".join(lines[size + 1 :]))
    # print("part1: ", result)
    # start = time.time()
    grid = lines[:size]
    for i in range(size):
        grid[i] = list(grid[i])
    print(grid)
    result = part2("".join(lines[size + 1 :]))
    print("part2: ", result)
    # 10385 too low
    # print("Runtime: ", time.time() - start)
