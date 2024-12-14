from pathlib import Path
import time
import re

parser = r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)"

sizeX = 101
sizeY = 103


def part1(robots):
    time = 100
    for robot in robots:
        x, y = robot[:2]
        vx, vy = robot[2:]
        x += time * vx
        y += time * vy
        robot[:2] = x % sizeX, y % sizeY

    q1 = sum(x < sizeX // 2 and y < sizeY // 2 for x, y, _, _ in robots)
    q2 = sum(x > sizeX // 2 and y < sizeY // 2 for x, y, _, _ in robots)
    q3 = sum(x < sizeX // 2 and y > sizeY // 2 for x, y, _, _ in robots)
    q4 = sum(x > sizeX // 2 and y > sizeY // 2 for x, y, _, _ in robots)
    return q1 * q2 * q3 * q4


def writeMap(robots, file):
    for y in range(sizeY):
        line = ""
        for x in range(sizeX):
            if [x, y] in [robot[:2] for robot in robots]:
                line += "#"
            else:
                line += "."
        file.write(line)
        file.write("\n")

    file.write("\n")


def printMap(robots):
    for y in range(sizeY):
        line = ""
        for x in range(sizeX):
            if [x, y] in [robot[:2] for robot in robots]:
                line += "#"
            else:
                line += "."
        print(line)


def part2(robots):
    timeToEasterEgg = 8179
    for robot in robots:
        x, y = robot[:2]
        vx, vy = robot[2:]
        x += timeToEasterEgg * vx
        y += timeToEasterEgg * vy
        robot[:2] = x % sizeX, y % sizeY

    printMap(robots)

    # for robot in robots:
    #     originalX, originalY = robot[:2]
    #     x, y = robot[:2]
    #     vx, vy = robot[2:]
    #     # Find looping frequency
    #     frequency = 0
    #     while True:
    #         frequency += 1
    #         x += vx
    #         y += vy
    #         x, y = x % sizeX, y % sizeY
    #         if x == originalX and y == originalY:
    #             robot.append(frequency)
    #             break
    # path = Path(__file__).parent / "./out.txt"
    # with path.open("w") as f:
    #     frequency = 10403
    #     for time in range(frequency):
    #         f.write(str(time))
    #         f.write("\n")
    #         for robot in robots:
    #             x, y = robot[:2]
    #             vx, vy = robot[2:]
    #             x += vx
    #             y += vy
    #             robot[:2] = x % sizeX, y % sizeY
    #         printMap(robots, f)

    return timeToEasterEgg


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    robots = []
    for line in lines:
        x, y, vx, vy = map(int, re.findall(parser, line)[0])
        robots.append([x, y, vx, vy])
    # printMap(robots)
    result = part1(robots)
    print("part1: ", result)
    # start = time.time()
    robots = []
    for line in lines:
        x, y, vx, vy = map(int, re.findall(parser, line)[0])
        robots.append([x, y, vx, vy])
    result = part2(robots)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
