from pathlib import Path

escaper = str.maketrans(
    {
        "\\": r"\\",
        '"': r"\"",
    }
)


def part1(lines):
    charCodes = 0
    nbChars = 0
    for line in lines:
        charCodes += len(line)
        nbChars += len(eval(line))
    return charCodes - nbChars


def part2(lines):
    charCodes = 0
    nbChars = 0
    for line in lines:
        charCodes += len(line)
        nbChars += len(line.translate(escaper)) + 2  # quotes
    return nbChars - charCodes


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    result = part1(lines.copy())
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
