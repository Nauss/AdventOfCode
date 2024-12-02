from pathlib import Path


def move(direction, position, houses):
    x, y = position
    if direction == "^":
        y += 1
    elif direction == "v":
        y -= 1
    elif direction == ">":
        x += 1
    elif direction == "<":
        x -= 1
    position = (x, y)
    houses[position] = houses.get(position, 0) + 1
    return position


def part1(directions):
    houses = {(0, 0): 1}
    position = (0, 0)
    for i, direction in enumerate(directions):
        position = move(direction, position, houses)
    return len(houses)


def part2(directions):
    houses = {(0, 0): 1}
    robotHouses = {(0, 0): 1}
    position = (0, 0)
    robotPosition = (0, 0)
    for i, direction in enumerate(directions):
        if i % 2 == 0:
            position = move(direction, position, houses)
        else:
            robotPosition = move(direction, robotPosition, robotHouses)

    return len(houses | robotHouses)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    directions = f.readlines()[0]
    result = part1(directions)
    print("part1: ", result)
    result = part2(directions)
    print("part2: ", result)
