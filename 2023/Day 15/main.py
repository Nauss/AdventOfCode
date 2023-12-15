import copy
from pathlib import Path
import re
import time
import numpy as np

multiplier = 17
output_size = 256


def hash(string):
    result = 0
    for i in range(len(string)):
        result = ((result + ord(string[i])) * multiplier) % output_size
    return result


def part1(sequence):
    result = 0
    for string in sequence:
        result += hash(string)
    return result


split_step = re.compile(r"(.*)[=-](\d*)")


def index(box, label):
    for i in range(len(box)):
        if box[i][0] == label:
            return i
    return -1


def remove(box, label):
    for i in range(len(box)):
        if box[i][0] == label:
            box.pop(i)
            return


def part2(sequence, boxes):
    for string in sequence:
        match = split_step.match(string)
        label = match.group(1)
        value = int(match.group(2) or -1)
        box_index = hash(label)
        if box_index not in boxes:
            boxes[box_index] = []
        box = boxes[box_index]
        index_label = index(box, label)
        if value > 0:  # =
            if index_label == -1:
                box.append((label, value))
            else:
                box[index_label] = (label, value)
        else:  # -
            if index_label != -1:
                remove(box, label)
    result = 0
    for box_number, box in boxes.items():
        if len(box) == 0:
            continue
        for lens_index, (label, value) in enumerate(box):
            result += (box_number + 1) * (lens_index + 1) * value
    return result


path = Path(__file__).parent / "./data.txt"
with path.open() as f:
    # Read line
    sequence = f.readline().strip().split(",")
    result = part1(sequence)
    print("part1: ", result)
    t = time.time()
    boxes = {}
    result = part2(sequence, boxes)
    print(f"part2 {time.time() - t}: ", result)
