from pathlib import Path


def add(values):
    result = 0
    for v in values[:-1]:
        result += int(v)
    return result


def mul(values):
    result = int(values[0])
    for v in values[1:-1]:
        result *= int(v)
    return result


def compute(lines, col):
    if lines[-1][col] == "+":
        return add([l[col] for l in lines])
    else:
        return mul([l[col] for l in lines])


def part1(lines):
    lines = [line.split() for line in lines]
    nb_cols = len(lines[0])
    result = 0
    for i in range(nb_cols):
        result += compute(lines, i)
    return result


def get_number(lines, col):
    number = ""
    for i in range(len(lines)):
        d = lines[i][col]
        if d == " " or d == "*" or d == "+":
            continue
        number += d
    return number


def add2(values):
    result = 0
    for v in values:
        result += int(v)
    return result


def mul2(values):
    result = int(values[0])
    for v in values[1:]:
        result *= int(v)
    return result


def part2(lines):
    starts = []
    for i in range(len(lines[-1])):
        if lines[-1][i] == "+":
            starts.append((i, "+"))
        if lines[-1][i] == "*":
            starts.append((i, "*"))

    result = 0
    for col, type in starts:
        numbers = []
        current_col = col
        current = get_number(lines, current_col)
        while current != "":
            numbers.append(current)
            current_col += 1
            if current_col >= len(lines[0]):
                break
            current = get_number(lines, current_col)
        if type == "+":
            result += add2(numbers)
        else:
            result += mul2(numbers)
    return result


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    clean_lines = []
    for line in lines:
        clean_lines.append(line.replace("\n", ""))
    result = part2(clean_lines)
    print("part2: ", result)
