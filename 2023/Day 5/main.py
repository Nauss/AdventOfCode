from pathlib import Path
import math


class GardenMap:
    def __init__(self, name):
        self.name = name
        self.sources = []
        self.destinations = []
        self.lengths = []

    def __str__(self):
        return f"{self.name}: sources: {self.sources} destinations: {self.destinations} lengths: {self.lengths}"

    def read(self, line):
        destination, source, length = line.strip().split(" ")
        self.destinations.append(int(destination))
        self.sources.append(int(source))
        self.lengths.append(int(length))

    def destination(self, seed):
        distances = [seed - source for source in self.sources]
        positive_distances = []
        for index, distance in enumerate(distances):
            if distance >= 0 and distance <= self.lengths[index]:
                positive_distances.append(distance)
        if len(positive_distances) == 0:
            return seed
        distance = min(positive_distances)
        index = distances.index(distance)
        return self.destinations[index] + distance

    def source(self, seed):
        distances = [seed - destination for destination in self.destinations]
        positive_distances = []
        for index, distance in enumerate(distances):
            if distance >= 0 and distance <= self.lengths[index]:
                positive_distances.append(distance)
        if len(positive_distances) == 0:
            return seed
        distance = min(positive_distances)
        index = distances.index(distance)
        return self.sources[index] + distance


def parse(f):
    maps = []
    seeds = [int(seed) for seed in f.readline().split(":")[1].strip().split(" ")]
    f.readline()
    while True:
        map = GardenMap(f.readline().split(" ")[0])
        line = f.readline()
        if not line:
            break
        while line and line != "\n":
            map.read(line)
            line = f.readline()
        maps.append(map)

    return (seeds, maps)


def part1(seeds, maps):
    location = math.inf
    for seed in seeds:
        for map in maps:
            seed = map.destination(seed)
        if seed < location:
            location = seed

    return location


def check(seed, seeds):
    for i in range(0, len(seeds), 2):
        possibilities = range(seeds[i], seeds[i] + seeds[i + 1])
        if seed in possibilities:
            return True
    return False


def part2(seeds, maps):
    for index in range(17700000, 17800000):
        fake_seed = index
        for map in reversed(maps):
            fake_seed = map.source(fake_seed)

        if check(fake_seed, seeds):
            return index


# Open data.txt file
path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read all lines
    (seeds, maps) = parse(f)
    result = part1(seeds, maps)
    print("part1: ", result)
    result = part2(seeds, maps)
    print("part2: ", result)
