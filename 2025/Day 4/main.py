from pathlib import Path

directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]


def check_bounds(grid, row, col):
    nb_rows = len(grid)
    nb_cols = len(grid[0])
    return row >= 0 and col >= 0 and row < nb_rows and col < nb_cols


def neighbor_rolls(grid, row, col):
    rolls = 0
    for direction in directions:
        check_row = row + direction[0]
        check_col = col + direction[1]
        if not check_bounds(grid, check_row, check_col):
            continue
        if grid[check_row][check_col] == "@":
            rolls += 1
    return rolls


def part1(grid):
    count = 0
    nb_rows = len(grid)
    nb_cols = len(grid[0])
    for row in range(nb_rows):
        for col in range(nb_cols):
            if grid[row][col] == "@" and neighbor_rolls(grid, row, col) < 4:
                count += 1
    return count


def remove(grid):
    removed = 0
    nb_rows = len(grid)
    nb_cols = len(grid[0])
    for row in range(nb_rows):
        for col in range(nb_cols):
            if grid[row][col] == "@" and neighbor_rolls(grid, row, col) < 4:
                grid[row][col] = "x"
                removed += 1
    return removed


def part2(grid):
    total = 0
    removed = remove(grid)
    while removed != 0:
        total += removed
        removed = remove(grid)
    return total


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    grid = [list(line.strip()) for line in f.readlines()]
    result = part1(grid)
    print("part1: ", result)
    result = part2(grid)
    print("part2: ", result)
