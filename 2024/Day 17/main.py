from pathlib import Path
import time


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


# Inverse instructions
def adv_inv(memory):
    combo = getCombo(memory)
    memory["A"] = memory["A"] * pow(2, combo)
    memory["pc"] -= 2


def bxl_inv(memory):
    memory["B"] = memory["B"] ^ getLiteral(memory)
    memory["pc"] -= 2


def bst_inv(memory):
    combo = getCombo(memory)
    memory["B"] = combo % 8
    memory["pc"] -= 2


def jnz_inv(memory):
    if memory["A"] == 0:
        memory["pc"] -= 2
    else:
        memory["pc"] = getLiteral(memory)


def bxc_inv(memory):
    memory["B"] = memory["B"] ^ memory["C"]
    memory["pc"] -= 2


def out_inv(memory):
    combo = getCombo(memory)
    del memory["output"][-1]
    memory["pc"] -= 2


def bdv_inv(memory):
    combo = getCombo(memory)
    memory["B"] = memory["A"] * pow(2, combo)
    memory["pc"] -= 2


def cdv_inv(memory):
    combo = getCombo(memory)
    memory["C"] = memory["A"] * pow(2, combo)
    memory["pc"] -= 2


def part1():
    memory = {
        "A": 33940147,
        "B": 0,
        "C": 0,
        "program": [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0],
        "pc": 0,
        "output": [],
    }
    memory = {
        "A": 117440,
        "B": 0,
        "C": 0,
        "program": [0, 3, 5, 4, 3, 0],
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

    return ",".join([str(o) for o in memory["output"]])


def part2():
    memory = {
        "A": 10,
        "B": 0,
        "C": 0,
        "program": [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0],
        "pc": 0,
        "output": [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0],
    }
    # memory = {
    #     "A": 0,
    #     "B": 0,
    #     "C": 0,
    #     "program": [0, 3, 5, 4, 3, 0],
    #     "pc": 0,
    #     "output": [0, 3, 5, 4, 3, 0],
    # }
    memory["pc"] = len(memory["output"]) - 1
    program = memory["program"]
    while memory["pc"] >= 0:
        if program[memory["pc"]] == 0:
            adv_inv(memory)
        elif program[memory["pc"]] == 1:
            bxl_inv(memory)
        elif program[memory["pc"]] == 2:
            bst_inv(memory)
        elif program[memory["pc"]] == 3:
            jnz_inv(memory)
        elif program[memory["pc"]] == 4:
            bxc_inv(memory)
        elif program[memory["pc"]] == 5:
            out_inv(memory)
        elif program[memory["pc"]] == 6:
            bdv_inv(memory)
        elif program[memory["pc"]] == 7:
            cdv_inv(memory)

    return ",".join([str(o) for o in memory["output"]])


# Open data.txt file
# memory = {
#     "A": 729,
#     "B": 0,
#     "C": 0,
#     "program": [0, 1, 5, 4, 3, 0],
#     "pc": 0,
#     "output": [],
# }
# result = part1()
# print("part1: ", result)
# start = time.time()
result = part2()
print("part2: ", result)
# print("Runtime: ", time.time() - start)
# 33940147 too low
