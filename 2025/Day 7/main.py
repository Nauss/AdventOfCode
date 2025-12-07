from pathlib import Path


def part1(lines):
    start_col = lines[0].index("S")
    splits = 0
    beams = {0: set(), 1: set([start_col])}
    for row in range(2, len(lines) - 1):
        beams[row] = set()
        for b in beams[row - 1]:
            if lines[row][b] == "^":
                beams[row].add(b - 1)
                beams[row].add(b + 1)
                splits += 1
            else:
                beams[row].add(b)
    return splits


def part2(lines):
    clean_lines = []
    for i in range(0, len(lines), 2):
        clean_lines.append(lines[i])
    start_col = clean_lines[0].index("S")
    beams = {0: set([start_col])}
    for row in range(1, len(clean_lines)):
        beams[row] = set()
        for b in beams[row - 1]:
            if clean_lines[row][b] == "^":
                beams[row].add(b - 1)
                beams[row].add(b + 1)
            else:
                beams[row].add(b)

    first = beams[0].pop()
    timelines = {first: 1}
    for i in range(1, len(beams)):
        new_timelines = {}
        for b in beams[i]:
            for last in timelines:
                if (
                    clean_lines[i][last] == "^" and (b == last - 1 or b == last + 1)
                ) or last == b:
                    if b in new_timelines:
                        new_timelines[b] += timelines[last]
                    else:
                        new_timelines[b] = timelines[last]
        timelines = new_timelines
    count = 0
    for timeline in timelines:
        count += timelines[timeline]
    return count


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    result = part1(lines)
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
