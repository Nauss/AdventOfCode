from pathlib import Path
import re

parser = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def part1(expression):
    matches = parser.findall(expression)
    print("matches: ", matches)
    result = 0
    for a, b in matches:
        result += int(a) * int(b)
    return result


parser2 = re.compile(r"((do\(\)|don't\(\))|mul\((\d{1,3}),(\d{1,3})\))")


def part2(expression):
    matches = parser2.findall(expression)
    print("matches: ", matches)
    result = 0
    enabled = True
    for match in matches:
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:
            result += int(match[2]) * int(match[3])
    return result


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = ""
    for line in f.readlines():
        lines += line.strip()
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
