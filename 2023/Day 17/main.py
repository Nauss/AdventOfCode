import copy
import functools
from pathlib import Path
import time
import numpy as np
from enum import Enum


def next_direction(previous, current):
    if previous == current:
        return "-"
    if previous[0] == current[0]:
        if previous[1] < current[1]:
            return ">"
        else:
            return "<"
    else:
        if previous[0] < current[0]:
            return "v"
        else:
            return "^"


def must_turn(next, previous, direction):
    minus_one = previous[next]
    if minus_one == None:
        return False
    minus_two = previous[minus_one]
    if minus_two == None:
        return False
    minus_tree = previous[minus_two]
    if minus_tree == None:
        return False
    if (
        direction[minus_one]
        == direction[minus_two]
        == direction[minus_tree]
        == next_direction(minus_one, next)
    ):
        return True


def find_min(Q, distance, previous, direction):
    min = np.inf
    summit = None
    for s in Q:
        if distance[s] < min:
            if must_turn(s, previous, direction):
                continue
            min = distance[s]
            summit = s
    return summit


def update_distance(grid, distance, previous, direction, s1, s2):
    if distance[s2] > distance[s1] + grid[s2]:
        distance[s2] = distance[s1] + grid[s2]
        previous[s2] = s1
        direction[s2] = next_direction(s1, s2)


def get_neighbors(grid, position):
    neighbors = []
    if position[0] > 0:
        neighbors.append((position[0] - 1, position[1]))
    if position[0] < grid.shape[0] - 1:
        neighbors.append((position[0] + 1, position[1]))
    if position[1] > 0:
        neighbors.append((position[0], position[1] - 1))
    if position[1] < grid.shape[1] - 1:
        neighbors.append((position[0], position[1] + 1))
    return neighbors


def part1(grid):
    start_position = (0, 0)
    end_position = (grid.shape[0] - 1, grid.shape[1] - 1)

    # Dijkstra
    distance = np.full(grid.shape, np.inf)
    previous = np.full(grid.shape, None)
    direction = grid.astype(str)
    Q = set()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            Q.add((i, j))
    distance[start_position] = 0
    direction[start_position] = ">"

    u = start_position
    while len(Q) > 0:
        u = find_min(Q, distance, previous, direction)
        if u == end_position:
            break
        Q.remove(u)

        neighbors = get_neighbors(grid, u)
        for v in neighbors:
            update_distance(grid, distance, previous, direction, u, v)

    # Print the path
    path = grid.astype(str)
    path[start_position] = direction[start_position]
    path[end_position] = direction[end_position]
    current = previous[end_position]
    result = grid[start_position]
    while current != start_position:
        path[current] = direction[current]
        result += grid[current]
        current = previous[current]
    print(path)
    print(distance)
    print(direction)

    return result


def part2(grid):
    result = 0
    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read lines
    grid = np.array([[int(c) for c in line.strip()] for line in f.readlines()])
    t = time.time()
    result = part1(grid)
    print(f"part1 {time.time() - t}: ", result)
    # t = time.time()
    # result = part2(grid)
    # print(f"part2 {time.time() - t}: ", result)
