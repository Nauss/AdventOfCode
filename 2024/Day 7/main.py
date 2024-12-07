from pathlib import Path
import sys
import time

sys.setrecursionlimit(1000000)


def numberToBinary(n, length, nbOperators):
    if nbOperators == 2:
        return format(n, "b").zfill(length)
    elif nbOperators == 3:
        if n == 0:
            return "0" * length
        digits = "012"
        result = ""
        while n > 0:
            result = digits[n % nbOperators] + result
            n //= nbOperators
    return result.zfill(length)


def compute(inputs, operators, nbOperators):
    result = inputs[0]
    for index, operator in enumerate(
        numberToBinary(operators, len(inputs) - 1, nbOperators)
    ):
        if operator == "0":
            result += inputs[index + 1]
        elif operator == "1":
            result *= inputs[index + 1]
        elif operator == "2":
            result = int(str(result) + str(inputs[index + 1]))
    return result


def solve(result, inputs, operators, nbOperators):
    currentResult = compute(inputs, operators, nbOperators)
    # print(operators, numberToBinary(operators, len(inputs) - 1, nbOperators))
    if currentResult == result:
        return result
    elif operators > 0:
        solved = solve(result, inputs, operators - 1, nbOperators)
        if solved != 0:
            return solved
    return 0


def part1(lines):
    sum = 0
    nbOperators = 2
    for line in lines:
        result = int(line[0][:-1])
        inputs = [int(x) for x in line[1:]]
        operators = int("1" * (len(inputs) - 1), nbOperators)
        sum += solve(result, inputs, operators, nbOperators)

    return sum


def part2(lines):
    sum = 0
    nbOperators = 3
    for line in lines:
        result = int(line[0][:-1])
        inputs = [int(x) for x in line[1:]]
        operators = int("2" * (len(inputs) - 1), nbOperators)
        sum += solve(result, inputs, operators, nbOperators)

    return sum


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip(":\n").split() for line in f]
    result = part1(lines)
    print("part1: ", result)
    start = time.time()
    result = part2(lines)
    print("Runtime: ", time.time() - start)
    print("part2: ", result)
