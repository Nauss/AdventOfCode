import copy
from pathlib import Path
import re
import time
import numpy as np

direction_lookup = {
    "right": 1,
    "left": 2,
    "up": 4,
    "down": 8,
}
beams = []
result_grid = []


class Beam:
    direction = "right"
    position = {"row": 0, "col": 0}

    def __init__(self, grid, row=0, col=0, direction="right"):
        self.grid = grid
        self.direction = direction
        self.position = {"row": row, "col": col}

    def move(self):
        global result_grid
        if self.check_loop():
            return False

        is_not_point = self.grid[self.position["row"]][self.position["col"]] != "."
        if is_not_point:
            result_grid[self.position["row"]][self.position["col"]] += direction_lookup[
                self.direction
            ]
        else:
            result_grid[self.position["row"]][self.position["col"]] += 1

        if is_not_point:
            self.change_direction()

        if self.direction == "right":
            self.position["col"] += 1
        elif self.direction == "left":
            self.position["col"] -= 1
        elif self.direction == "up":
            self.position["row"] -= 1
        elif self.direction == "down":
            self.position["row"] += 1

        if (
            self.position["row"] < 0
            or self.position["col"] < 0
            or self.position["row"] >= len(self.grid)
            or self.position["col"] >= len(self.grid[0])
        ):
            return False

        return True

    def change_direction(self):
        global beams
        if self.grid[self.position["row"]][self.position["col"]] == "/":
            if self.direction == "right":
                self.direction = "up"
            elif self.direction == "left":
                self.direction = "down"
            elif self.direction == "up":
                self.direction = "right"
            elif self.direction == "down":
                self.direction = "left"
        elif self.grid[self.position["row"]][self.position["col"]] == "\\":
            if self.direction == "right":
                self.direction = "down"
            elif self.direction == "left":
                self.direction = "up"
            elif self.direction == "up":
                self.direction = "left"
            elif self.direction == "down":
                self.direction = "right"
        elif self.grid[self.position["row"]][self.position["col"]] == "|":
            if self.direction == "right":
                self.direction = "up"
                new_beam = Beam(self.grid)
                new_beam.position = {
                    "row": self.position["row"] + 1,
                    "col": self.position["col"],
                }
                new_beam.direction = "down"
                beams.append(new_beam)
            elif self.direction == "left":
                self.direction = "down"
                new_beam = Beam(self.grid)
                new_beam.position = {
                    "row": self.position["row"] - 1,
                    "col": self.position["col"],
                }
                new_beam.direction = "up"
                beams.append(new_beam)
        elif self.grid[self.position["row"]][self.position["col"]] == "-":
            if self.direction == "up":
                self.direction = "left"
                new_beam = Beam(self.grid)
                new_beam.position = {
                    "row": self.position["row"],
                    "col": self.position["col"] + 1,
                }
                new_beam.direction = "right"
                beams.append(new_beam)
            elif self.direction == "down":
                self.direction = "right"
                new_beam = Beam(self.grid)
                new_beam.position = {
                    "row": self.position["row"],
                    "col": self.position["col"] - 1,
                }
                new_beam.direction = "left"
                beams.append(new_beam)

    def check_loop(self):
        global result_grid
        loop = False
        if (
            self.position["row"] < 0
            or self.position["col"] < 0
            or self.position["row"] >= len(self.grid)
            or self.position["col"] >= len(self.grid[0])
        ):
            return True
        if self.grid[self.position["row"]][self.position["col"]] != ".":
            value = result_grid[self.position["row"]][self.position["col"]]
            loop = direction_lookup[self.direction] & value
        return loop


def part1(grid):
    global beams
    global result_grid
    result_grid = np.array([[0 for _ in range(len(grid[0]))] for _ in range(len(grid))])
    beams = [Beam(grid)]
    while len(beams) > 0:
        for beam in beams:
            if not beam.move():
                beams.remove(beam)

    print(repr(result_grid))
    return np.count_nonzero(
        result_grid,
    )


def part2(grid):
    global beams
    global result_grid
    nb_rows = len(grid)
    nb_cols = len(grid[0])
    all_beams = []
    for r in range(nb_rows):
        all_beams.append(Beam(grid, r, 0, "right"))
        all_beams.append(Beam(grid, r, nb_cols - 1, "left"))
    for c in range(nb_cols):
        all_beams.append(Beam(grid, 0, c, "down"))
        all_beams.append(Beam(grid, nb_rows - 1, c, "up"))

    result = 0
    for b in all_beams:
        beams = [b]
        result_grid = np.zeros_like(grid, dtype=np.uint8)
        while len(beams) > 0:
            for beam in beams:
                if not beam.move():
                    beams.remove(beam)

        result = max(result, np.count_nonzero(result_grid))

    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read lines
    grid = np.array([[c for c in line.strip()] for line in f.readlines()])
    result = part1(grid)
    print("part1: ", result)
    t = time.time()
    result = part2(grid)
    print(f"part2 {time.time() - t}: ", result)
