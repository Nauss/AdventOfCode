from pathlib import Path
import time


def part1(lines):
    antennas = {}
    sizeY = len(lines)
    sizeX = len(lines[0])
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))

    antinodes = {}
    for antenna, positions in antennas.items():
        # For each pair of positions
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                position1 = positions[i]
                position2 = positions[j]
                # Compute the distance between the two positions
                distance = (
                    position1[0] - position2[0],
                    position1[1] - position2[1],
                )
                # Add the distance to each position and check if inside the grid
                antinode1 = (position1[0] + distance[0], position1[1] + distance[1])
                antinode2 = (position2[0] - distance[0], position2[1] - distance[1])
                if (
                    antinode1[0] >= 0
                    and antinode1[0] < sizeX
                    and antinode1[1] >= 0
                    and antinode1[1] < sizeY
                ):
                    if antinode1 not in antinodes:
                        antinodes[antinode1] = []
                    antinodes[antinode1].append(antenna)
                if (
                    antinode2[0] >= 0
                    and antinode2[0] < sizeX
                    and antinode2[1] >= 0
                    and antinode2[1] < sizeY
                ):
                    if antinode2 not in antinodes:
                        antinodes[antinode2] = []
                    antinodes[antinode2].append(antenna)

    return len(antinodes)


def addNode(antinodes, position, antenna):
    if position not in antinodes:
        antinodes[position] = []
    antinodes[position].append(antenna)


def isInside(position, size):
    return (
        position[0] >= 0
        and position[0] < size
        and position[1] >= 0
        and position[1] < size
    )


def part2(lines):
    antennas = {}
    size = len(lines)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))

    antinodes = {}
    for antenna, positions in antennas.items():
        # For each pair of positions
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                position1 = positions[i]
                position2 = positions[j]
                # Compute the distance between the two positions
                distance = (
                    position1[0] - position2[0],
                    position1[1] - position2[1],
                )
                addNode(antinodes, position1, antenna)
                addNode(antinodes, position2, antenna)
                # Add the distance to each position and check if inside the grid
                antinode1 = (position1[0] + distance[0], position1[1] + distance[1])
                antinode2 = (position2[0] - distance[0], position2[1] - distance[1])
                antinode1Inside = isInside(antinode1, size)
                antinode2Inside = isInside(antinode2, size)
                while antinode1Inside or antinode2Inside:
                    if antinode1Inside:
                        addNode(antinodes, antinode1, antenna)
                    if antinode2Inside:
                        addNode(antinodes, antinode2, antenna)
                    antinode1 = (antinode1[0] + distance[0], antinode1[1] + distance[1])
                    antinode2 = (antinode2[0] - distance[0], antinode2[1] - distance[1])
                    antinode1Inside = isInside(antinode1, size)
                    antinode2Inside = isInside(antinode2, size)

    return len(antinodes)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    result = part1(lines)
    print("part1: ", result)
    # start = time.time()
    result = part2(lines)
    # print("Runtime: ", time.time() - start)
    print("part2: ", result)
