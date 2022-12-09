use std::{collections::HashMap, f64::consts::SQRT_2};

#[derive(PartialEq, Eq, Hash, Clone)]
struct Position {
    x: i32,
    y: i32,
}

impl Position {
    fn distance(self: &Position, p2: &Position) -> f64 {
        let x = self.x - p2.x;
        let y = self.y - p2.y;
        ((x * x + y * y) as f64).sqrt()
    }
    fn move_knot(self: &Position, other: &mut Position) {
        let dist = self.distance(other);
        if dist > SQRT_2 {
            let mut x = 0;
            if self.x > other.x {
                x = 1;
            } else if self.x < other.x {
                x = -1;
            }
            let mut y = 0;
            if self.y > other.y {
                y = 1;
            } else if self.y < other.y {
                y = -1;
            }
            other.x += x;
            other.y += y;
        }
    }
    fn move_knots(self: &Position, knots: &mut Vec<Position>) {
        let mut previous = self.clone();
        knots.iter_mut().for_each(|knot| {
            previous.move_knot(knot);
            previous = knot.clone();
        });
    }
}

fn apply(
    movement: &(&str, i32),
    head: &mut Position,
    tail: &mut Vec<Position>,
    visited: &mut HashMap<Position, bool>,
) {
    match movement {
        ("R", distance) => {
            for _ in 0..*distance {
                head.x += 1;
                head.move_knots(tail);
                visited.entry(tail.last().unwrap().clone()).or_insert(true);
            }
        }
        ("L", distance) => {
            for _ in 0..*distance {
                head.x -= 1;
                head.move_knots(tail);
                visited.entry(tail.last().unwrap().clone()).or_insert(true);
            }
        }
        ("U", distance) => {
            for _ in 0..*distance {
                head.y += 1;
                head.move_knots(tail);
                visited.entry(tail.last().unwrap().clone()).or_insert(true);
            }
        }
        ("D", distance) => {
            for _ in 0..*distance {
                head.y -= 1;
                head.move_knots(tail);
                visited.entry(tail.last().unwrap().clone()).or_insert(true);
            }
        }
        _ => panic!("Invalid movement"),
    }
}

fn main() {
    let movements = include_str!("../data.txt")
        .lines()
        .map(|line| {
            let mut splitted = line.split(" ");
            let direction = splitted.next().unwrap();
            let distance = splitted.next().unwrap().parse::<i32>().unwrap();
            (direction, distance)
        })
        .collect::<Vec<_>>();

    let mut head = Position { x: 0, y: 0 };
    let mut tail = vec![Position { x: 0, y: 0 }];
    let mut visited = HashMap::new();
    movements.iter().for_each(|movement| {
        apply(&movement, &mut head, &mut tail, &mut visited);
    });
    println!("Part 1: {}", visited.iter().count()); // 6243

    let mut head = Position { x: 0, y: 0 };
    let mut tail = vec![Position { x: 0, y: 0 }; 9];
    let mut visited = HashMap::new();
    movements.iter().for_each(|movement| {
        apply(&movement, &mut head, &mut tail, &mut visited);
    });
    println!("Part 2: {}", visited.iter().count()); // 2630
}
