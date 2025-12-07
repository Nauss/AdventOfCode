from pathlib import Path


def in_range(ranges, value):
    for range in ranges:
        if value >= range[0] and value <= range[1]:
            return True
    return False


def part1(ranges, ids):
    fresh = 0
    for id in ids:
        if in_range(ranges, id):
            fresh += 1
    return fresh


def merge_ranges(ranges):
    new_ranges = []
    ranges.sort()
    for range in ranges:
        start = range[0]
        end = range[1]
        found = False
        for new_range in new_ranges:
            if start >= new_range[0] and start <= new_range[1]:
                found = True
                if end > new_range[1]:
                    new_range[1] = end
            elif end >= new_range[0] and end <= new_range[1]:
                found = True
                if start < new_range[0]:
                    new_range[0] = start
        if not found:
            new_ranges.append(range)
    return new_ranges


def part2(ranges):
    merged = merge_ranges(ranges)
    fresh = 0
    for range in merged:
        fresh += range[1] - range[0] + 1
    return fresh


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    ranges = []
    ids = []
    is_range = True
    for line in f.readlines():
        line = line.strip()
        if line == "":
            is_range = False
            continue
        if is_range:
            splitted = line.split("-")
            ranges.append([int(splitted[0]), int(splitted[1])])
        else:
            ids.append(int(line))
    result = part1(ranges, ids)
    print("part1: ", result)
    result = part2(ranges)
    print("part2: ", result)
