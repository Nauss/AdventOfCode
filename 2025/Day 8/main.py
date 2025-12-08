from pathlib import Path


class Box:
    x = 0
    y = 0
    z = 0

    def __init__(self, position):
        positions = position.split(",")
        self.x = int(positions[0])
        self.y = int(positions[1])
        self.z = int(positions[2])

    def distance(self, other):
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)


def add_connection(circuits, connection):
    box1 = connection[0]
    box2 = connection[1]
    circuit1 = None
    circuit2 = None
    for circuit in circuits:
        if box1 in circuit:
            circuit1 = circuit
        if box2 in circuit:
            circuit2 = circuit
        if circuit1 != None and circuit2 != None:
            break

    if circuit1 == None and circuit2 == None:
        circuits.append([box1, box2])
    elif circuit1 == circuit2:
        return False
    elif circuit1 != None and circuit2 != None:
        # merge
        for c in circuit2:
            if not c in circuit1:
                circuit1.append(c)
        circuits.remove(circuit2)
    elif circuit1 != None:
        circuit1.append(box2)
    else:
        circuit2.append(box1)

    return True


def part1(boxes):
    distances = {}
    circuits = []
    for box1 in boxes:
        circuits.append([box1])
        for box2 in boxes:
            if box1 == box2 or (box2, box1) in distances:
                continue
            distance = box1.distance(box2)
            distances[(box1, box2)] = distance

    distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    dist_keys = list(distances.keys())
    current_connection = 0
    while current_connection < 1000:
        connection = dist_keys[current_connection]
        add_connection(circuits, connection)
        current_connection += 1

    circuits = sorted(circuits, key=len, reverse=True)
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])


def part2(boxes):
    distances = {}
    circuits = []
    for box1 in boxes:
        circuits.append([box1])
        for box2 in boxes:
            if box1 == box2 or (box2, box1) in distances:
                continue
            distance = box1.distance(box2)
            distances[(box1, box2)] = distance

    distances = dict(sorted(distances.items(), key=lambda item: item[1]))
    dist_keys = list(distances.keys())
    current_connection = 0
    while True:
        connection = dist_keys[current_connection]
        add_connection(circuits, connection)
        current_connection += 1
        if current_connection > 2 and len(circuits) == 1:
            return connection[0].x * connection[1].x


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    lines = [line.strip() for line in f.readlines()]
    boxes = []
    for line in lines:
        box = Box(line)
        boxes.append(box)
    result = part1(boxes)
    print("part1: ", result)
    result = part2(boxes)
    print("part2: ", result)
