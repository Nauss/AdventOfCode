from pathlib import Path

vowels = "aeiou"
forbidden = ["ab", "cd", "pq", "xy"]


def checkVowels(line):
    return sum([line.count(v) for v in vowels]) >= 3


def checkDoubleLetter(line):
    for i in range(len(line) - 1):
        if line[i] == line[i + 1]:
            return True
    return False


def checkForbidden(line):
    for f in forbidden:
        if f in line:
            return False
    return True


def part1(lines):
    niceSum = 0
    for line in lines:
        if checkVowels(line) and checkDoubleLetter(line) and checkForbidden(line):
            niceSum += 1
    return niceSum


def checkDoublePair(line):
    for i in range(len(line) - 3):
        if line[i : i + 2] in line[i + 2 :]:
            return True
    return False


def checkMirrorLetter(line):
    for i in range(len(line) - 2):
        if line[i] == line[i + 2]:
            return True
    return False


def part2(lines):
    niceSum = 0
    for line in lines:
        if checkDoublePair(line) and checkMirrorLetter(line):
            niceSum += 1
    return niceSum


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
