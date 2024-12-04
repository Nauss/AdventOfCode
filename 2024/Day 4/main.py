from pathlib import Path


def mDirections(grid, x, y):
    lastX = len(grid[0]) - 1
    lastY = len(grid) - 1
    directions = []
    # up
    if y > 0 and grid[y - 1][x] == "M":
        directions.append("up")
    # down
    if y < lastY and grid[y + 1][x] == "M":
        directions.append("down")
    # left
    if x > 0 and grid[y][x - 1] == "M":
        directions.append("left")
    # right
    if x < lastX and grid[y][x + 1] == "M":
        directions.append("right")
    # up left
    if y > 0 and x > 0 and grid[y - 1][x - 1] == "M":
        directions.append("up left")
    # up right
    if y > 0 and x < lastX and grid[y - 1][x + 1] == "M":
        directions.append("up right")
    # down left
    if y < lastY and x > 0 and grid[y + 1][x - 1] == "M":
        directions.append("down left")
    # down right
    if y < lastY and x < lastX and grid[y + 1][x + 1] == "M":
        directions.append("down right")

    return directions


def checkAS(grid, x, y, direction):
    lastX = len(grid[0]) - 1
    lastY = len(grid) - 1
    if direction == "up":
        if y > 1 and grid[y - 1][x] == "A" and grid[y - 2][x] == "S":
            return True
    if direction == "down":
        if y < lastY - 1 and grid[y + 1][x] == "A" and grid[y + 2][x] == "S":
            return True
    if direction == "left":
        if x > 1 and grid[y][x - 1] == "A" and grid[y][x - 2] == "S":
            return True
    if direction == "right":
        if x < lastX - 1 and grid[y][x + 1] == "A" and grid[y][x + 2] == "S":
            return True
    if direction == "up left":
        if y > 1 and x > 1 and grid[y - 1][x - 1] == "A" and grid[y - 2][x - 2] == "S":
            return True
    if direction == "up right":
        if (
            y > 1
            and x < lastX - 1
            and grid[y - 1][x + 1] == "A"
            and grid[y - 2][x + 2] == "S"
        ):
            return True
    if direction == "down left":
        if (
            y < lastY - 1
            and x > 1
            and grid[y + 1][x - 1] == "A"
            and grid[y + 2][x - 2] == "S"
        ):
            return True
    if direction == "down right":
        if (
            y < lastY - 1
            and x < lastX - 1
            and grid[y + 1][x + 1] == "A"
            and grid[y + 2][x + 2] == "S"
        ):
            return True
    return False


def move(x, y, direction):
    if direction == "up":
        y -= 1
    if direction == "down":
        y += 1
    if direction == "left":
        x -= 1
    if direction == "right":
        x += 1
    if direction == "up left":
        y -= 1
        x -= 1
    if direction == "up right":
        y -= 1
        x += 1
    if direction == "down left":
        y += 1
        x -= 1
    if direction == "down right":
        y += 1
        x += 1
    return x, y


def checkPart1(grid, x, y):
    directions = mDirections(grid, x, y)
    nbXmas = 0
    for direction in directions:
        xM, yM = move(x, y, direction)
        if checkAS(grid, xM, yM, direction):
            nbXmas += 1
    return nbXmas


def part1(grid):
    width = len(grid[0])
    height = len(grid)
    result = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "X":
                result += checkPart1(grid, x, y)

    return result


def checkPart2(grid, x, y):
    topLeft = grid[y - 1][x - 1]
    topRight = grid[y - 1][x + 1]
    bottomLeft = grid[y + 1][x - 1]
    bottomRight = grid[y + 1][x + 1]
    if (
        (topLeft == "M" and bottomRight == "S")
        or (topLeft == "S" and bottomRight == "M")
    ) and (
        (topRight == "M" and bottomLeft == "S")
        or (topRight == "S" and bottomLeft == "M")
    ):
        return True


def part2(grid):
    width = len(grid[0])
    height = len(grid)
    result = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == "A" and checkPart2(grid, x, y):
                result += 1

    return result


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [line.strip() for line in f.readlines()]
    result = part1(grid)
    print("part1: ", result)
    result = part2(grid)
    print("part2: ", result)
