use std::collections::HashSet;

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct Position {
    x: i32,
    y: i32,
}

impl Position {
    fn distance(&self, point: &Position) -> f64 {
        let x = self.x - point.x;
        let y = self.y - point.y;
        (x * x + y * y) as f64
    }
    fn move_knot(&self, other: &mut Position) {
        let dist = self.distance(other);
        if dist > 2.0 {
            let x = (self.x - other.x).signum();
            let y = (self.y - other.y).signum();
            other.x += x;
            other.y += y;
        }
    }
    fn move_knots(&self, knots: &mut [Position]) {
        let mut previous = self;
        knots.iter_mut().for_each(|knot| {
            previous.move_knot(knot);
            previous = knot;
        });
    }
}

fn apply(
    movement: &(&str, i32),
    head: &mut Position,
    tail: &mut [Position],
    visited: &mut HashSet<Position>,
) {
    let head_mover: fn(&mut Position) = match movement.0 {
        "R" => |head| head.x += 1,
        "L" => |head| head.x -= 1,
        "U" => |head| head.y += 1,
        "D" => |head| head.y -= 1,
        _ => panic!("Invalid movement"),
    };
    let mut do_move = || {
        head_mover(head);
        head.move_knots(tail);
        visited.insert(*tail.last().unwrap());
    };

    for _ in 0..movement.1 {
        do_move();
    }
}

fn main() {
    let movements = include_str!("../data.txt")
        .lines()
        .map(|line| {
            let mut splitted = line.split(' ');
            let direction = splitted.next().unwrap();
            let distance = splitted.next().unwrap().parse::<i32>().unwrap();
            (direction, distance)
        })
        .collect::<Vec<_>>();

    let mut head = Position { x: 0, y: 0 };
    let mut tail = vec![Position { x: 0, y: 0 }];
    let mut visited = HashSet::new();
    movements.iter().for_each(|movement| {
        apply(movement, &mut head, &mut tail, &mut visited);
    });
    println!("Part 1: {}", visited.len()); // 6243

    let mut head = Position { x: 0, y: 0 };
    let mut tail = vec![Position { x: 0, y: 0 }; 9];
    let mut visited = HashSet::new();
    movements.iter().for_each(|movement| {
        apply(movement, &mut head, &mut tail, &mut visited);
    });
    println!("Part 2: {}", visited.len()); // 2630
}
