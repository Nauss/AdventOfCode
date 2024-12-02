from pathlib import Path
import hashlib


def part1(secret):
    number = 0
    while True:
        hash = hashlib.md5((secret + str(number)).encode()).hexdigest()
        if hash.startswith("00000"):
            return number
        number += 1


def part2(directions):
    number = 0
    while True:
        hash = hashlib.md5((secret + str(number)).encode()).hexdigest()
        if hash.startswith("000000"):
            return number
        number += 1


secret = "iwrupvqb"
result = part1(secret)
print("part1: ", result)
result = part2(secret)
print("part2: ", result)
