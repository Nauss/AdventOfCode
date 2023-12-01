from pathlib import Path
import re


def part1(line):
    cleaned = re.sub("[a-zA-Z]", "", line.strip())
    if len(cleaned) == 0:
        return 0
    result = cleaned[0]
    if len(cleaned) > 1:
        result += cleaned[len(cleaned) - 1]
    else:
        result += result

    # Convert to int
    return int(result)


numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
letterNumberRegex = re.compile(r"(\d|" + "|".join(numbers.keys()) + r")")
reveresedLetterNumberRegex = re.compile(
    r"(\d|" + "|".join([number[::-1] for number in numbers.keys()]) + r")"
)


def getDigit(line, reverse=False):
    regex = reveresedLetterNumberRegex if reverse else letterNumberRegex
    letterMatch = regex.search(line[::-1] if reverse else line)
    digit = None
    if letterMatch is not None:
        [start, end] = letterMatch.span()
        if end - start > 1:
            digit = numbers[letterMatch[1][::-1] if reverse else letterMatch[1]]
        else:
            digit = letterMatch[1]
    return digit


def part2(line):
    line = line.strip()
    first = getDigit(line)
    last = getDigit(line, True)
    if last is None:
        last = first

    return int(first + last)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = f.readlines()
    result = [part1(line) for line in lines]
    print("part1: ", sum(result))
    result = [part2(line) for line in lines]
    print("part2: ", sum(result))
