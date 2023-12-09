from pathlib import Path


def get_diff(history, index):
    if index >= len(history) - 1:
        return 0
    return history[index] - history[index + 1]


def check_upper_diffs(diffs, level, diff):
    history = diff["history"]
    index = diff["index"]
    if level > 0 and index + 1 >= len(history):
        upper_diff = diffs[level - 1]
        upper_diff["index"] += 1
        if upper_diff["index"] + 1 >= len(upper_diff["history"]):
            check_upper_diffs(diffs, level - 1, upper_diff)
        history.append(get_diff(upper_diff["history"], upper_diff["index"]))
        diffs[level] = diff


def part1(histories):
    result = 0
    for history in histories:
        diffs = {}
        level = 0
        diff = {
            "history": history,
            "index": 0,
        }
        diffs[level] = diff
        while True:
            history = diff["history"]
            index = diff["index"]
            check_upper_diffs(diffs, level, diff)
            diff = {
                "history": [get_diff(history, index)],
                "index": 0,
            }
            if 1 in diffs and len(diffs[1]["history"]) == len(diffs[0]["history"]) - 1:
                break
            level += 1
            diffs[level] = diff
        next_value = 0
        for l in range(level - 1, -1, -1):
            next_value += diffs[l]["history"][0]
        result += next_value

    return result


def part2(histories):
    result = 0
    for history in histories:
        diffs = {}
        level = 0
        diff = {
            "history": history,
            "index": 0,
        }
        diffs[level] = diff
        while True:
            history = diff["history"]
            index = diff["index"]
            check_upper_diffs(diffs, level, diff)
            diff = {
                "history": [get_diff(history, index)],
                "index": 0,
            }
            if 1 in diffs and len(diffs[1]["history"]) == len(diffs[0]["history"]) - 1:
                break
            level += 1
            diffs[level] = diff
        next_value = 0
        for l in range(level - 1, -1, -1):
            next_value = diffs[l]["history"][-1] - next_value
        result += next_value

    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    histories = [line.strip().split(" ") for line in f.readlines()]
    histories = [[int(i) for i in reversed(line)] for line in histories]
    result = part1(histories)
    print("part1: ", result)
    result = part2(histories)
    print("part2: ", result)
