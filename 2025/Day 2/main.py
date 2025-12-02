from pathlib import Path


def check_range1(range):
    [current, max] = range
    max = int(max)

    count = 0
    current_number = int(current)
    while current_number <= max:
        half_size = len(current) // 2

        # Must be even
        if 2 * half_size != len(current):
            current = "1" + "0" * len(current)
            current_number = int(current)
            continue

        first, second = current[:half_size], current[half_size:]
        if first == second:
            count += current_number
            current = str(int(first) + 1) * 2
            current_number = int(current)
        else:
            if int(first) > int(second):
                current = first * 2
                current_number = int(current)
            else:
                current = str(int(first) + 1) * 2
                current_number = int(current)

    return count


def part1(line):
    ranges = [r.split("-") for r in line]
    count = 0
    for r in ranges:
        count += check_range1(r)
    return count


def check_number(number, size):
    reference = number[:size]
    for i in range(size, len(number), size):
        if reference != number[i : i + size]:
            return False
    return True


def check_range2(input):
    [current, max] = input
    max = int(max)

    count = 0
    current_number = int(current)
    while current_number <= max:
        half_size = len(current) // 2
        for i in range(1, half_size + 1):
            if check_number(current, i):
                count += current_number
                break
        current_number += 1
        current = str(current_number)

    return count


def part2(line):
    ranges = [r.split("-") for r in line]
    count = 0
    for r in ranges:
        count += check_range2(r)
    return count


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read line
    line = f.readline().strip().split(",")
    result = part1(line)
    print("part1: ", result)
    result = part2(line)
    print("part2: ", result)
