from pathlib import Path


def part1(lines):
    circuit = {}
    currentLine = 0
    while len(lines) > 0:
        line = lines[currentLine]
        executed = False
        if len(line) == 3:
            if line[0].isdigit():
                circuit[line[2]] = int(line[0])
                executed = True
            elif line[0] in circuit:
                circuit[line[2]] = circuit[line[0]]
                executed = True
        elif len(line) == 4:
            if line[1] in circuit:
                circuit[line[3]] = ~circuit[line[1]]
                executed = True
        else:
            if line[0].isdigit() and line[2] in circuit:
                circuit[line[4]] = int(line[0]) & circuit[line[2]]
                executed = True
            elif line[0] in circuit:
                if line[1] == "AND" and line[2] in circuit:
                    circuit[line[4]] = circuit[line[0]] & circuit[line[2]]
                    executed = True
                elif line[1] == "OR" and line[2] in circuit:
                    circuit[line[4]] = circuit[line[0]] | circuit[line[2]]
                    executed = True
                elif line[1] == "LSHIFT":
                    circuit[line[4]] = circuit[line[0]] << int(line[2])
                    executed = True
                elif line[1] == "RSHIFT":
                    circuit[line[4]] = circuit[line[0]] >> int(line[2])
                    executed = True

        if executed:
            lines.pop(currentLine)
            currentLine = 0
        else:
            currentLine += 1
    return circuit["a"]


def part2(lines):
    circuit = {"b": 46065}
    currentLine = 0
    while len(lines) > 0:
        line = lines[currentLine]
        executed = False
        if len(line) == 3:
            if line[0].isdigit():
                circuit[line[2]] = int(line[0])
                executed = True
            elif line[0] in circuit:
                circuit[line[2]] = circuit[line[0]]
                executed = True
        elif len(line) == 4:
            if line[1] in circuit:
                circuit[line[3]] = ~circuit[line[1]]
                executed = True
        else:
            if line[0].isdigit() and line[2] in circuit:
                circuit[line[4]] = int(line[0]) & circuit[line[2]]
                executed = True
            elif line[0] in circuit:
                if line[1] == "AND" and line[2] in circuit:
                    circuit[line[4]] = circuit[line[0]] & circuit[line[2]]
                    executed = True
                elif line[1] == "OR" and line[2] in circuit:
                    circuit[line[4]] = circuit[line[0]] | circuit[line[2]]
                    executed = True
                elif line[1] == "LSHIFT":
                    circuit[line[4]] = circuit[line[0]] << int(line[2])
                    executed = True
                elif line[1] == "RSHIFT":
                    circuit[line[4]] = circuit[line[0]] >> int(line[2])
                    executed = True

        if executed:
            lines.pop(currentLine)
            currentLine = 0
        else:
            currentLine += 1
    return circuit["a"]


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip().split() for line in f.readlines()]
    result = part1(lines.copy())
    print("part1: ", result)
    result = part2(lines)
    print("part2: ", result)
