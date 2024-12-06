from pathlib import Path


def turnRight(direction):
    if direction == (0, -1):
        return (1, 0)
    if direction == (1, 0):
        return (0, 1)
    if direction == (0, 1):
        return (-1, 0)
    if direction == (-1, 0):
        return (0, -1)


def part1(grid):
    visited = set()
    position = (91, 69)  # (x, y)
    direction = (0, -1)
    while True:
        visited.add(position)
        x, y = (a + b for a, b in zip(position, direction))
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            break
        if grid[y][x] == "#":
            direction = turnRight(direction)
            continue

        position = (x, y)

    return len(visited)


def doMove(grid, obstaclePosition):
    obstaclePosition = (obstaclePosition[0] + 1, obstaclePosition[1])
    if obstaclePosition[0] >= len(grid[0]):
        obstaclePosition = (0, obstaclePosition[1] + 1)
        if obstaclePosition[1] >= len(grid):
            return None
    return obstaclePosition


def moveObstacle(grid, obstaclePosition):
    # Reset the old position
    grid[obstaclePosition[1]][obstaclePosition[0]] = "."
    # Move the obstacle
    obstaclePosition = doMove(grid, obstaclePosition)
    while (
        obstaclePosition != None
        and grid[obstaclePosition[1]][obstaclePosition[0]] == "#"
    ):
        obstaclePosition = doMove(grid, obstaclePosition)

    if obstaclePosition == None:
        return None

    # Set the new position
    grid[obstaclePosition[1]][obstaclePosition[0]] = "#"
    return obstaclePosition


def part2(grid):
    obstaclePosition = (0, 0)
    grid[obstaclePosition[1]][obstaclePosition[0]] = "#"
    nbLoops = 0
    while True:
        visited = set()
        position = (91, 69)  # (x, y)
        direction = (0, -1)
        while True:
            if position + direction in visited:
                nbLoops += 1
                break
            visited.add(position + direction)
            x, y = (a + b for a, b in zip(position, direction))
            if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
                break
            if grid[y][x] == "#":
                direction = turnRight(direction)
                continue

            position = (x, y)

        obstaclePosition = moveObstacle(grid, obstaclePosition)
        if obstaclePosition == None:
            break

    return nbLoops


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [list(line.strip()) for line in f]
    result = part1(grid)
    print("part1: ", result)
    result = part2(grid)
    print("part2: ", result)
