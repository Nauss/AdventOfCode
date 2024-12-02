from pathlib import Path
import re


def part1(instructions):
    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    for instruction in instructions:
        action, start, end = instruction
        doAction = lambda action, current: (
            1 if action == "turn on" else 0 if action == "turn off" else 1 - current
        )
        for i in range(start[0], end[0] + 1):
            for j in range(start[1], end[1] + 1):
                result = doAction(action, lights[i][j])
                lights[i][j] = result
    return sum([sum(row) for row in lights])


def part2(instructions):
    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    for instruction in instructions:
        action, start, end = instruction
        doAction = lambda action, current: (
            current + 1
            if action == "turn on"
            else max(0, current - 1) if action == "turn off" else current + 2
        )
        for i in range(start[0], end[0] + 1):
            for j in range(start[1], end[1] + 1):
                result = doAction(action, lights[i][j])
                lights[i][j] = result
    return sum([sum(row) for row in lights])


parser = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")
# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    instructions = []
    for line in lines:
        match = parser.match(line)
        instructions.append(
            [
                match.group(1),
                (int(match.group(2)), int(match.group(3))),
                (int(match.group(4)), int(match.group(5))),
            ]
        )
    result = part1(instructions)
    print("part1: ", result)
    result = part2(instructions)
    print("part2: ", result)
