use std::collections::{HashSet, VecDeque};

#[derive(Hash, PartialEq, Eq, Clone, Copy, Debug)]
struct Position {
    row: usize,
    col: usize,
}

impl Position {
    fn new(row: usize, col: usize) -> Position {
        Position { row, col }
    }
}

enum Direction {
    Up,
    Down,
    Left,
    Right,
}
const DIRECTIONS: [Direction; 4] = [
    Direction::Up,
    Direction::Down,
    Direction::Left,
    Direction::Right,
];

fn main() {
    let (starts, end, grid) = parse();

    let part1 = a_star(&starts[0], &end, &grid);
    println!("Part 1: {}", part1); // 383

    let part2 = starts
        .iter()
        .map(|start| a_star(start, &end, &grid))
        .min()
        .unwrap();
    println!("Part 2: {}", part2); // 377
}

fn a_star(start: &Position, end: &Position, grid: &grid::Grid<usize>) -> isize {
    // a star
    let mut queue: VecDeque<(Position, isize)> = VecDeque::new();
    let mut visited = HashSet::new();
    queue.push_back((*start, 0));
    visited.insert(*start);
    while let Some((position, steps)) = queue.pop_front() {
        if position == *end {
            return steps;
        }
        let current_value = grid.get(position.row, position.col).unwrap();
        for direction in DIRECTIONS.iter() {
            let next = next_pos(&position, direction);
            if next.is_none() {
                continue;
            }
            let next = next.unwrap();
            let next_value = grid.get(next.row, next.col);
            if next_value.is_some()
                && *next_value.unwrap() as isize - *current_value as isize <= 1
                && !visited.contains(&next)
            {
                visited.insert(next);
                queue.push_back((next, steps + 1));
            }
        }
    }
    isize::MAX
}

fn next_pos(position: &Position, direction: &Direction) -> Option<Position> {
    match direction {
        Direction::Up => {
            if position.row == 0 {
                None
            } else {
                Some(Position::new(position.row - 1, position.col))
            }
        }
        Direction::Down => Some(Position::new(position.row + 1, position.col)),
        Direction::Left => {
            if position.col == 0 {
                None
            } else {
                Some(Position::new(position.row, position.col - 1))
            }
        }
        Direction::Right => Some(Position::new(position.row, position.col + 1)),
    }
}

fn parse() -> (Vec<Position>, Position, grid::Grid<usize>) {
    let mut width = 0;
    let mut starts = Vec::new();
    let mut end = Position { row: 0, col: 0 };
    let mut content = Vec::new();
    let lines = include_str!("../data.txt").lines();
    for (row, line) in lines.enumerate() {
        if row == 0 {
            width = line.len();
        }
        let chars = line.chars();
        for (col, c) in chars.enumerate() {
            if c == 'S' {
                starts.insert(0, Position { row, col });
                content.push(0);
            } else if c == 'a' {
                starts.push(Position { row, col });
                content.push(0);
            } else if c == 'E' {
                end = Position { row, col };
                content.push(('z' as usize) - ('a' as usize));
            } else {
                content.push((c as usize) - ('a' as usize));
            }
        }
    }
    (starts, end, grid::Grid::from_vec(content, width))
}
