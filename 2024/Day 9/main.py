from pathlib import Path
import time


def getSystem(diskMap):
    index = 0
    id = 0
    system = []
    while index < len(diskMap):
        file = int(diskMap[index])
        freeSpace = int(diskMap[index + 1]) if index + 1 < len(diskMap) else 0
        system.extend([id for _ in range(file)])
        system.extend(["." for _ in range(freeSpace)])

        id += 1
        index += 2

    return system


def compressPart1(system):
    compressed = []
    reverseIndex = len(system) - 1
    for i in range(0, len(system)):
        if i > reverseIndex:
            break
        if system[i] != ".":
            compressed.append(system[i])
            continue
        compressed.append(system[reverseIndex])
        reverseIndex -= 1
        while system[reverseIndex] == ".":
            reverseIndex -= 1

    return compressed


def computeCheckSum(system):
    sum = 0
    for i in range(len(system)):
        if system[i] != ".":
            sum += system[i] * i

    return sum


def part1(diskMap):
    system = getSystem(diskMap)
    compressed = compressPart1(system)

    return computeCheckSum(compressed)


def getFileLength(system, index):
    id = system[index]
    count = 0
    while index >= 0 and system[index] == id:
        count += 1
        index -= 1

    return count


def findFreeSpace(compressed, count):
    index = 0
    freeSize = count
    while index < len(compressed):
        if compressed[index] == ".":
            freeSize -= 1
            if freeSize == 0:
                break
        else:
            freeSize = count
        index += 1

    return index + 1 - count if freeSize == 0 else -1


def compressPart2(system):
    compressed = system
    index = len(system) - 1
    testedIds = set()
    while index >= 0:
        current = system[index]
        if current == ".":
            index -= 1
            continue
        if current in testedIds:
            index -= 1
            continue
        testedIds.add(current)
        count = getFileLength(system, index)
        freeSpaceIndex = findFreeSpace(compressed, count)
        if freeSpaceIndex != -1 and freeSpaceIndex < index:
            for c in range(count):
                compressed[freeSpaceIndex + c] = current
                compressed[index - c] = "."
        index -= count

    return compressed


def part2(diskMap):
    system = getSystem(diskMap)
    compressed = compressPart2(system)

    return computeCheckSum(compressed)


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    diskMap = [line.strip() for line in f][0]
    result = part1(diskMap)
    print("part1: ", result)
    # start = time.time()
    result = part2(diskMap)
    print("part2: ", result)
    # print("Runtime: ", time.time() - start)
