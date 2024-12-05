from pathlib import Path
import sys

sys.setrecursionlimit(10000)


def check(rules, update):
    valuesBefore = set()
    for updateValue in update:
        if not updateValue in rules:
            valuesBefore.add(updateValue)
            continue
        if len(rules[updateValue] & valuesBefore):
            return False
        valuesBefore.add(updateValue)
    return True


def part1(rules, updates):
    sum = 0
    for update in updates:
        if check(rules, update):
            middleIndex = int((len(update) - 1) / 2)
            sum += update[middleIndex]

    return sum


def placeBefore(update, index1, index2):
    if index1 == index2:
        return
    if index1 > index2:
        index1, index2 = index2, index1
    return (
        update[:index1]
        + [update[index2]]
        + [update[index1]]
        + update[index1 + 1 : index2]
        + update[index2 + 1 :]
    )


def check2(rules, update, depth=0):
    if depth > 9500:
        print("Too deep", update)
        return False
    valuesBefore = set()
    for updateValue in update:
        if not updateValue in rules:
            valuesBefore.add(updateValue)
            continue
        errors = list(rules[updateValue] & valuesBefore)
        errors.sort()
        if len(errors):
            for error in errors:
                update = placeBefore(
                    update, update.index(updateValue), update.index(error)
                )
            return check2(rules, update, depth + 1)
        valuesBefore.add(updateValue)
    return update[int((len(update) - 1) / 2)] if depth > 0 else False


def part2(rules, updates):
    sum = 0
    for update in updates:
        result = check2(rules, update)
        if result:
            sum += result

    return sum


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    rules = {}
    updates = []
    parsingRules = True
    for line in lines:
        if not line:
            parsingRules = False
            continue
        if parsingRules:
            before, after = [int(x) for x in line.split("|")]
            if not before in rules:
                rules[before] = set()
            rules[before].add(after)
        else:
            updates.append([int(x) for x in line.split(",")])
    result = part1(rules, updates)
    print("part1: ", result)
    result = part2(rules, updates)
    print("part2: ", result)
