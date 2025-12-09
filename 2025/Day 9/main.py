from pathlib import Path


def part1(positions):
    max_area = 0
    for tile1 in positions:
        for tile2 in positions:
            x1, y1 = tile1
            x2, y2 = tile2
            area = abs(x1 - x2 + 1) * abs(y1 - y2 + 1)
            if area > max_area:
                max_area = area
    return max_area


def is_inside(positions, position):
    x = position[0]
    y = position[1]

    inside = False
    for i in range(len(positions)):
        xi = positions[i][0]
        yi = positions[i][1]
        xj = positions[i - 1][0]
        yj = positions[i - 1][1]

        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi) + xi
        )
        if intersect:
            inside = not inside

    return inside


def part2(positions):
    max_area = 0
    for tile1 in positions:
        for tile2 in positions:
            x1, y1 = tile1
            x2, y2 = tile2
            # Make sure that all the edges have red or green tiles
            edge_points = []
            for x in range(min(x1, x2), max(x1, x2)):
                edge_points.append([x, y1])
                edge_points.append([x, y2])
            for y in range(min(y1, y2), max(y1, y2)):
                edge_points.append([x1, y])
                edge_points.append([x2, y])
            if not all(
                [is_inside(positions, edge_point) for edge_point in edge_points]
            ):
                continue
            area = abs(tile1[0] - tile2[0] + 1) * abs(tile1[1] - tile2[1] + 1)
            if area > max_area:
                max_area = area
    return max_area


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    positions = [[int(i) for i in line.strip().split(",")] for line in f.readlines()]
    result = part1(positions)
    print("part1: ", result)
    result = part2(positions)
    print("part2: ", result)
