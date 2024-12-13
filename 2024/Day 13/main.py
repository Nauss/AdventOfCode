from pathlib import Path
import time
import re

# PX = AX * a + BX * b
# PY = AY * a + BY * b

# a = (PX - BX * b) / AX
# PY = AY * ((PX - BX * b) / AX) + BY * b
# PY = AY * PX / AX - AY * BX * b / AX + BY * b
# PY - AY * PX / AX = (BY - AY * BX / AX) * b
# b = (PY - AY * PX / AX) / (BY - AY * BX / AX)

# a = (PY - BY * b) / AY
# PX = AX * ((PY - BY * b) / AY) + BX * b
# PX = AX * PY / AY - AX * BY / AY * b  + BX * b
# PX - AX * PY / AY = (BX - AX * BY / AY) * b
# b = (PX - AX * PY / AY) / (BX - AX * BY / AY)

# b = (PX - AX * a) / BX
# PY = AY * a + BY * ((PX - AX * a) / BX)
# PY = AY * a + BY * PX / BX - BY * AX / BX * a
# PY - BY * PX / BX = (AY - BY * AX / BX) * a
# a = (PY - BY * PX / BX) / (AY - BY * AX / BX)

# b = (PY - AY * a) / BY
# PX = AX * a + BX * ((PY - AY * a) / BY)
# PX = AX * a + BX * PY / BY - BX * AY / BY * a
# PX - BX * PY / BY = (AX - BX * AY / BY) * a
# a = (PX - BX * PY / BY) / (AX - BX * AY / BY)

eps = 0.001


def part1(arcades):
    tokens = 0
    for arcade in arcades:
        AX = arcade["AX"]
        AY = arcade["AY"]
        BX = arcade["BX"]
        BY = arcade["BY"]
        PX = arcade["PX"]
        PY = arcade["PY"]
        A1 = (PY - BY * PX / BX) / (AY - BY * AX / BX)
        A2 = (PX - BX * PY / BY) / (AX - BX * AY / BY)
        B1 = (PX - AX * PY / AY) / (BX - AX * BY / AY)
        B2 = (PY - AY * PX / AX) / (BY - AY * BX / AX)
        if (
            abs(A1 - round(A1)) < eps
            and abs(A2 - round(A2)) < eps
            and abs(B1 - round(B1)) < eps
            and abs(B2 - round(B2)) < eps
        ):
            tokens += min(A1 * 3 + B1, A2 * 3 + B2)
        else:
            if abs(A1 - int(A1)) < eps and abs(B1 - int(B1)) < eps:
                tokens += A1 * 3 + B1
            elif abs(A2 - int(A2)) < eps and abs(B2 - int(B2)) < eps:
                tokens += A2 * 3 + B2
    return int(tokens)


def part2(arcades):
    tokens = 0
    for arcade in arcades:
        AX = arcade["AX"]
        AY = arcade["AY"]
        BX = arcade["BX"]
        BY = arcade["BY"]
        PX = arcade["PX"] + 10000000000000
        PY = arcade["PY"] + 10000000000000
        A1 = (PY - BY * PX / BX) / (AY - BY * AX / BX)
        A2 = (PX - BX * PY / BY) / (AX - BX * AY / BY)
        B1 = (PX - AX * PY / AY) / (BX - AX * BY / AY)
        B2 = (PY - AY * PX / AX) / (BY - AY * BX / AX)
        if A1 < 0 or A2 < 0 or B1 < 0 or B2 < 0:
            continue
        if (
            abs(A1 - round(A1)) < eps
            and abs(A2 - round(A2)) < eps
            and abs(B1 - round(B1)) < eps
            and abs(B2 - round(B2)) < eps
        ):
            tokens += min(A1 * 3 + B1, A2 * 3 + B2)
        else:
            if abs(A1 - int(A1)) < eps and abs(B1 - int(B1)) < eps:
                tokens += A1 * 3 + B1
            elif abs(A2 - int(A2)) < eps and abs(B2 - int(B2)) < eps:
                tokens += A2 * 3 + B2
            else:
                pass
    return int(tokens)


buttonA = r"Button A: X\+(\d+), Y\+(\d+)"
buttonB = r"Button B: X\+(\d+), Y\+(\d+)"
prize = r"Prize: X=(\d+), Y=(\d+)"
# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f]
    # Parse data
    arcades = []
    for i in range(0, len(lines), 4):
        m = re.match(buttonA, lines[i])
        AX = int(m.group(1))
        AY = int(m.group(2))
        m = re.match(buttonB, lines[i + 1])
        BX = int(m.group(1))
        BY = int(m.group(2))
        m = re.match(prize, lines[i + 2])
        PX = int(m.group(1))
        PY = int(m.group(2))
        arcades.append(({"AX": AX, "AY": AY, "BX": BX, "BY": BY, "PX": PX, "PY": PY}))

    result = part1(arcades)
    print("part1: ", result)
    # start = time.time()
    result = part2(arcades)
    print("part2: ", result)
    # 53642576199196 too low
    # print("Runtime: ", time.time() - start)
