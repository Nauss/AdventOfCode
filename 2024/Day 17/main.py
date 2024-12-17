from pathlib import Path
import time
import functools


# Utils
def getCombo(memory):
    operand = memory["program"][memory["pc"] + 1]
    if operand == 4:
        return memory["A"]
    elif operand == 5:
        return memory["B"]
    elif operand == 6:
        return memory["C"]
    else:
        return operand


def setCombo(memory, value):
    operand = memory["program"][memory["pc"] + 1]
    if operand == 4:
        memory["A"] = value
    elif operand == 5:
        memory["B"] = value
    elif operand == 6:
        memory["C"] = value


def getLiteral(memory):
    return memory["program"][memory["pc"] + 1]


# Instructions
def adv(memory):
    combo = getCombo(memory)
    memory["A"] = memory["A"] // pow(2, combo)
    memory["pc"] += 2


def bxl(memory):
    memory["B"] = memory["B"] ^ getLiteral(memory)
    memory["pc"] += 2


def bst(memory):
    combo = getCombo(memory)
    memory["B"] = combo % 8
    memory["pc"] += 2


def jnz(memory):
    if memory["A"] == 0:
        memory["pc"] += 2
    else:
        memory["pc"] = getLiteral(memory)


def bxc(memory):
    memory["B"] = memory["B"] ^ memory["C"]
    memory["pc"] += 2


def out(memory):
    combo = getCombo(memory)
    memory["output"].append(combo % 8)
    memory["pc"] += 2


def bdv(memory):
    combo = getCombo(memory)
    memory["B"] = memory["A"] // pow(2, combo)
    memory["pc"] += 2


def cdv(memory):
    combo = getCombo(memory)
    memory["C"] = memory["A"] // pow(2, combo)
    memory["pc"] += 2


def part1(start):
    memory = {
        "A": start,
        "B": 0,
        "C": 0,
        "program": [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0],
        "pc": 0,
        "output": [],
    }
    program = memory["program"]
    while memory["pc"] < len(program):
        if program[memory["pc"]] == 0:
            adv(memory)
        elif program[memory["pc"]] == 1:
            bxl(memory)
        elif program[memory["pc"]] == 2:
            bst(memory)
        elif program[memory["pc"]] == 3:
            jnz(memory)
        elif program[memory["pc"]] == 4:
            bxc(memory)
        elif program[memory["pc"]] == 5:
            out(memory)
        elif program[memory["pc"]] == 6:
            bdv(memory)
        elif program[memory["pc"]] == 7:
            cdv(memory)

    return memory["output"]


@functools.cache
def compute(A):
    B = A % 8
    B = B ^ 5
    C = A // pow(2, B)
    B = B ^ 6
    B = B ^ C
    return B % 8


def arrayEndsWith(array, end):
    for i in range(len(end)):
        if array[-1 - i] != end[-1 - i]:
            return False
    return True


def part2():
    goal = [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0]
    a = 0
    gc = len(goal) - 1
    while True:
        if compute(a) == goal[gc] and arrayEndsWith(goal, part1(a)):
            gc -= 1
            if gc == -1:
                return a
            a = 8 * a
            continue
        a += 1


# Open data.txt file

result = part1(33940147)
print("part1: ", result)
start = time.time()
result = part2()
print("part2: ", result)
print("Runtime: ", time.time() - start)
