from pathlib import Path

def max_in_range(joltages, start, end):
    active = joltages[start:end]
    value = max(active)
    index = start + active.index(value)
    return (value, index)


def get_max(line, required_digits):
    last_digit_index = required_digits - 1
    joltages = list(line)
    current_start = 0
    result = []
    while last_digit_index >= 0:
        m = max_in_range(joltages, current_start, len(joltages) - last_digit_index)
        current_start = m[1] + 1
        last_digit_index -= 1
        result.append(m[0])
    return int("".join(result))


def part1(lines):
    total = 0
    for line in lines:
        total += get_max(line, 2)
    return total


def part2(line):
    total = 0
    for line in lines:
        total += get_max(line, 12)
    return total


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
