import copy
from pathlib import Path
import re
import sys
import time
import numpy as np
from joblib import Parallel, delayed


def is_valid(rows, groups):
    row_index = 0
    group_index = 0
    while group_index < len(groups):
        group = groups[group_index]
        nb_valid = 0
        while row_index < len(rows):
            if rows[row_index] == "#":
                nb_valid += 1
                row_index += 1
            elif rows[row_index] == ".":
                if nb_valid != 0:
                    break
                row_index += 1

            if nb_valid >= group:
                break

        if nb_valid >= group:
            if row_index < len(rows):
                if rows[row_index] == "#":
                    # Not possible
                    return False
            group_index += 1
        else:
            return False

    while row_index < len(rows):
        if rows[row_index] == "#":
            return False
        row_index += 1
    return True


def brute_force(lines):
    results = []
    for line in lines:
        nb_secrets = line[0].count("?")
        nb_valid = 0
        for i in range(pow(2, nb_secrets)):
            bits = format(i, f"#0{nb_secrets+2}b")[2:]
            (rows, groups) = copy.deepcopy(line)
            for bit in bits:
                if bit == "1":
                    rows = rows.replace("?", "#", 1)
                else:
                    rows = rows.replace("?", ".", 1)
            if is_valid(rows, groups):
                nb_valid += 1

        results.append(nb_valid)

    return sum(results)


sys.setrecursionlimit(1000000)

permuts = []


def partial_test(groups, bits):
    partial_test = "^\.*"
    nb_bits = 0
    for group in groups:
        nb_bits += group
        if nb_bits > len(bits):
            partial_test += f"#{ {group - (nb_bits -len(bits))} }"
        elif nb_bits == len(bits):
            partial_test += f"#{ {group} }"
        else:
            partial_test += f"#{ {group} }\.\.*"
        if not re.search(partial_test, bits):
            return False
        nb_bits += 1
        if nb_bits >= len(bits):
            break
    return True


result = 0


def permutations(bits, test_solution):
    if "?" not in bits:
        global result
        result += 1
    else:
        new_bits = bits.replace("?", "#", 1)
        if re.match(test_solution, new_bits):
            permutations(new_bits, test_solution)
        new_bits = bits.replace("?", ".", 1)
        if re.match(test_solution, new_bits):
            permutations(new_bits, test_solution)


def compute_line(line):
    (rows, groups) = copy.deepcopy(line)
    test_solution = "^\.*"
    for group in groups:
        test_solution += f"(#|\?){ {group} }" + "(\.|\?)+"
    test_solution = test_solution[:-1] + "*"
    test_solution += "$"

    nb_secrets = rows.count("?")
    if nb_secrets == 0:
        return 1
    else:
        global result
        result = 0
        permutations("".join(rows), test_solution)
        return result


def compute(lines):
    results = [compute_line(line) for line in lines]
    # results = Parallel(n_jobs=4)(delayed(compute_line)(line) for line in lines)
    # for line in lines:
    #     (rows, groups) = copy.deepcopy(line)
    #     print(f"processing line {line_index} ({groups})")
    #     test_solution = ""
    #     for group in groups:
    #         test_solution += f"(#|\?){ {group} }" + "(\.|\?)+"
    #     test_solution = test_solution[:-1] + "*"

    #     for i in range(len(rows)):
    #         if rows[i] == "?":
    #             rows[i] = "#"
    #             hash_valid = re.search(test_solution, "".join(rows))
    #             rows[i] = "."
    #             dot_valid = re.search(test_solution, "".join(rows))
    #             if hash_valid and dot_valid:
    #                 rows[i] = "?"
    #             elif hash_valid:
    #                 rows[i] = "#"
    #             elif dot_valid:
    #                 rows[i] = "."

    #     test_solution = "^\.*"
    #     for group in groups:
    #         test_solution += f"#{ {group} }" + "\.+"
    #     test_solution = test_solution[:-1] + "*"
    #     test_solution += "$"

    #     nb_secrets = rows.count("?")
    #     if nb_secrets == 0:
    #         results.append(1)
    #     else:
    #         nb_valid = 0
    #         for i in range(pow(2, nb_secrets)):
    #             tested = "".join(rows)
    #             bits = format(i, f"#0{nb_secrets+2}b")[2:]
    #             for bit in bits:
    #                 if bit == "1":
    #                     tested = tested.replace("?", "#", 1)
    #                 else:
    #                     tested = tested.replace("?", ".", 1)
    #             if re.search(test_solution, tested):
    #                 nb_valid += 1

    #         results.append(nb_valid)

    #     print(rows)
    return sum(results)


def expand_line(line):
    result_array = np.repeat("".join(line[0]), 5)
    rows = list("?".join(result_array))
    groups = []
    for i in range(5):
        groups += line[1]
    return (rows, groups)


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split(" ") for line in f.readlines()]
    lines = [(list(line[0]), [int(c) for c in line[1].split(",")]) for line in lines]
    # lines = [(line[0], [int(c) for c in line[1].split(",")]) for line in lines]
    # result = brute_force(lines)
    # print("part1: ", result)
    t = time.time()
    expanded_lines = [expand_line(line) for line in lines]
    result = compute(expanded_lines)
    print(f"part2 {time.time() - t}: ", result)
