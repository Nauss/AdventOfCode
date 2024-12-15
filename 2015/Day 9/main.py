from pathlib import Path


def findConnection(city1, city2, connections):
    for connection in connections:
        if connection[0] == city1 and connection[1] == city2:
            return connection[2]
        if connection[1] == city1 and connection[0] == city2:
            return connection[2]
    return 0


minDistance = 100000
maxDistance = 0


def travel(city, cities, connections, visited, currentDistance):
    if len(visited) == len(cities):
        global minDistance
        global maxDistance
        if currentDistance < minDistance:
            minDistance = currentDistance
        if currentDistance > maxDistance:
            maxDistance = currentDistance
    for c in cities:
        if c not in visited:
            travel(
                c,
                cities,
                connections,
                [*visited, c],
                currentDistance + findConnection(city, c, connections),
            )


def part1(connections):
    cities = {}
    for connection in connections:
        if connection[0] not in cities:
            cities[connection[0]] = None
        if connection[1] not in cities:
            cities[connection[1]] = None

    cities = list(cities)

    for city in cities:
        travel(city, cities, connections, [city], 0)

    return minDistance


def part2():
    return maxDistance


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split() for line in f.readlines()]
    lines = [[line[0], line[2], int(line[4])] for line in lines]
    result = part1(lines.copy())
    print("part1: ", result)
    result = part2()
    print("part2: ", result)
