from pathlib import Path
import math

dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def inBounds(grid, pos):
    return (
        pos[0] > 0
        and pos[0] < len(grid[0]) - 1
        and pos[1] > 0
        and pos[1] < len(grid) - 1
    )


def shortestPath(cameFrom, current):
    path = []
    while current in cameFrom:
        path.append(current)
        current = cameFrom[current]
    path.reverse()
    return path


def getPossibleCheats(grid, current, cheats):
    for dir in dirs:
        x = current[0] + dir[0]
        y = current[1] + dir[1]
        if (
            x >= 0
            and x < len(grid[0]) - 1
            and y >= 0
            and y < len(grid) - 1
            and grid[y][x] == "#"
        ):
            cheats.add((x, y))


def distToEnd(start, endPos):
    return abs(start[0] - endPos[0]) + abs(start[1] - endPos[1])


cheated = []
cache = {}


def aStar(grid, startPos, endPos, cheatFromHere):
    global cheated
    global cache
    openSet = set()
    cameFrom = {}
    openSet.add(startPos)

    gScore = {}
    gScore[startPos] = 0

    fScore = {}
    fScore[startPos] = distToEnd(startPos, endPos)

    while len(openSet):
        current = min(openSet, key=lambda x: fScore[x])
        if current == endPos:
            result = shortestPath(cameFrom, current)
            return result

        openSet.remove(current)

        if cheatFromHere and current in cache:
            bestCache = cache[current]
            for others in openSet:
                if others in cache:
                    if len(cache[others]) < len(bestCache):
                        bestCache = cache[others]
            return bestCache

        for dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + dir[0], current[1] + dir[1])
            if (
                neighbor[0] <= 0
                or neighbor[0] >= len(grid[0]) - 1
                or neighbor[1] <= 0
                or neighbor[1] >= len(grid) - 1
            ):
                continue
            if neighbor == cheatFromHere:
                continue
            if grid[neighbor[1]][neighbor[0]] == "#":
                if not cheatFromHere:
                    result = aStar(grid, neighbor, endPos, current)
                    if result:
                        cameFrom[neighbor] = current
                        cheated.append(shortestPath(cameFrom, neighbor) + result)
                        del cameFrom[neighbor]
                continue
            tentative_gScore = gScore[current] + 1
            if tentative_gScore < gScore.get(neighbor, math.inf):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + distToEnd(neighbor, endPos)
                openSet.add(neighbor)

    return None


def printPath(grid, path):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in path:
                if grid[y][x] == "#":
                    print("1", end="")
                else:
                    print("X", end="")
            else:
                print(grid[y][x], end="")
        print()
    print()


def part1(grid):
    global cheated
    global cache

    startPos = None
    endPos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                startPos = (x, y)
            elif grid[y][x] == "E":
                endPos = (x, y)

    result = aStar(grid, startPos, endPos, True)
    printPath(grid, result)
    # Fill the cache
    for index, pos in enumerate(result):
        cache[pos] = result[index:]

    baseLine = len(result)
    result = aStar(grid, startPos, endPos, None)

    global cheated
    nbCheats = 0
    gains = {}
    for cheatedPath in cheated:
        gain = baseLine - len(cheatedPath)
        if gain >= 100:
            if gain not in gains:
                gains[gain] = 0
            gains[gain] += 1
            if gain == 2:
                print("gain " + str(gain))
                printPath(grid, cheatedPath)
            nbCheats += 1
        # printPath(grid, cheatedPath)
    return nbCheats


cheated2 = {}


def pathToString(path):
    # return "".join([str(pos[0]) + "," + str(pos[1]) for pos in path])
    return (
        str(path[0][0])
        + ","
        + str(path[0][1])
        + ","
        + str(path[-1][0])
        + ","
        + str(path[-1][1])
    )


def outside(grid, pos):
    return (
        pos[0] <= 0
        or pos[0] >= len(grid[0]) - 1
        or pos[1] <= 0
        or pos[1] >= len(grid) - 1
    )


def aStar2(
    grid, startPos, endPos, cheatFrom, currentCheats, cheatsCount=0, targetTime=math.inf
):
    if len(currentCheats) > targetTime:
        return None

    global cheated2
    global cache
    openSet = set()
    cameFrom = {}
    openSet.add(startPos)

    gScore = {}
    gScore[startPos] = 0

    fScore = {}
    fScore[startPos] = distToEnd(startPos, endPos)

    while len(openSet):
        current = min(openSet, key=lambda x: fScore[x])

        if current == endPos:
            result = shortestPath(cameFrom, current)
            return result

        openSet.remove(current)

        if cheatsCount != 19 and current in cache:
            bestCache = cache[current]
            for others in openSet:
                if others in cache:
                    if len(cache[others]) < len(bestCache):
                        bestCache = cache[others]
            return bestCache

        for dir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + dir[0], current[1] + dir[1])
            if outside(grid, neighbor):
                continue
            if grid[neighbor[1]][neighbor[0]] == "#":
                if cheatsCount > 0 and neighbor not in currentCheats:
                    newCurrentCheats = currentCheats.copy()
                    if len(newCurrentCheats) == 0:
                        newCurrentCheats = shortestPath(cameFrom, current)
                    newCurrentCheats.append(neighbor)
                    result = aStar2(
                        grid,
                        neighbor,
                        endPos,
                        current,
                        newCurrentCheats,
                        cheatsCount - 1,
                        targetTime,
                    )
                    if result:
                        if len(newCurrentCheats) + len(result) <= targetTime:
                            for pos in result:
                                newCurrentCheats.append(pos)
                            start = None
                            end = None
                            cheatLength = 0
                            for index, pos in enumerate(newCurrentCheats):
                                c = grid[pos[1]][pos[0]]
                                if c == "#":
                                    cheatLength += 1
                                if c == "#" and not start:
                                    if index > 0:
                                        start = newCurrentCheats[index - 1]
                                    else:
                                        start = (1, 3)
                                if c != "#" and start and not end:
                                    end = pos
                            if not end:
                                end = result[0]
                            cheatRange = (
                                " ".join(
                                    [str(x) + "," + str(y) for x, y in [start, end]]
                                )
                                + " "
                                + str(cheatLength)
                            )
                            # if cheatRange not in cheated2 or len(
                            #     newCurrentCheats
                            # ) < len(cheated2[cheatRange]):
                            if cheatRange in cheated2:
                                continue
                            cheated2[cheatRange] = newCurrentCheats

                continue
            tentative_gScore = gScore[current] + 1
            if tentative_gScore < gScore.get(neighbor, math.inf):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + distToEnd(neighbor, endPos)
                openSet.add(neighbor)

        # if len(currentCheats):
        #     cheatsCount = 0
    return None


def part2(grid):
    global cheated2
    global cache

    startPos = None
    endPos = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                startPos = (x, y)
            elif grid[y][x] == "E":
                endPos = (x, y)

    result = aStar2(grid, startPos, endPos, None, [], 0)
    printPath(grid, result)
    # Fill the cache
    for index, pos in enumerate(result):
        cache[pos] = result[index:]

    baseLine = len(result)
    expectedGain = 100
    result = aStar2(grid, startPos, endPos, None, [], 19, baseLine - expectedGain)

    nbCheats = 0
    gains = {}
    cheatedLength = {}
    for cheatedPath in cheated2.keys():
        s = baseLine - len(cheated2[cheatedPath])
        if s not in cheatedLength:
            cheatedLength[s] = []
        cheatedLength[s].append(cheatedPath)
    for cheatedPath in cheated2.values():
        gain = baseLine - len(cheatedPath)
        if gain >= expectedGain:
            if gain not in gains:
                gains[gain] = 0
            gains[gain] += 1
            if gain == 74:
                print("gain " + str(gain))
                printPath(grid, cheatedPath)
            nbCheats += 1
        # printPath(grid, cheatedPath)
    return nbCheats


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    grid = lines
    for i in range(len(grid)):
        grid[i] = list(grid[i])
    # result = part1(grid)
    # print("part1: ", result)
    # start = time.time()
    result = part2(grid)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
