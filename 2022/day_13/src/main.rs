use std::cmp::Ordering;

#[derive(Debug, PartialEq)]
enum Order {
    Right,
    Wrong,
    Equal,
}

struct Packet {
    line: Vec<char>,
    index: usize,
}

impl Packet {
    fn new(line: Vec<char>, index: usize) -> Self {
        Self { line, index }
    }
}

fn main() {
    // let left = "[1,[2,[3,[4,[5,6,7]]]],8,9]".chars().collect::<Vec<_>>();
    // let right = "[1,[2,[3,[4,[5,6,0]]]],8,9]".chars().collect::<Vec<_>>();
    // let left = "[[1],[2,3,4]]".chars().collect::<Vec<_>>();
    // let right = "[[1],4]".chars().collect::<Vec<_>>();
    // let left = "[[[]],[5,[[6,3,1],[5,1,3],1,[8,10,5,9,10]],7,6,[4,5,6,[]]]]"
    //     .chars()
    //     .collect::<Vec<_>>();
    // let right = "[[[]],[3,[[],[2,4,9,7,6],[1,9,10,1]],4,[2,[4],[],[0,1,9]],1],[],[1,7,2],[[7,[2,5,1,4],[],7,6]]]"
    //     .chars()
    //     .collect::<Vec<_>>();
    // println!(
    //     "{:?}",
    //     compare(&Packet::new(left, 0), &Packet::new(right, 0))
    // );
    let mut lines = include_str!("../data.txt")
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| line.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();
    let mut part1 = Vec::new();
    for i in (0..lines.len()).step_by(2) {
        let left = &lines[i];
        let right = &lines[i + 1];
        let result = compare(
            &Packet::new(left.clone(), 0),
            &Packet::new(right.clone(), 0),
        );
        part1.push(result);
    }
    println!("Part 1: {:?}", part1);
    println!(
        "Part 1: {:?}",
        part1.iter().enumerate().fold(0, |acc, (i, x)| acc
            + match x {
                Order::Right => i + 1,
                _ => 0,
            })
    );

    let two = vec!['[', '[', '2', ']', ']'];
    let six = vec!['[', '[', '6', ']', ']'];
    lines.insert(0, two.clone());
    lines.insert(6, six.clone());
    lines.sort_by(
        |a, b| match compare(&Packet::new(a.clone(), 0), &Packet::new(b.clone(), 0)) {
            Order::Right => std::cmp::Ordering::Less,
            Order::Wrong => std::cmp::Ordering::Greater,
            Order::Equal => std::cmp::Ordering::Equal,
        },
    );

    let tow_pos = lines
        .iter()
        .position(|x| x.cmp(&two) == Ordering::Equal)
        .unwrap();
    let six_pos = lines
        .iter()
        .position(|x| x.cmp(&six) == Ordering::Equal)
        .unwrap();

    // let mut part2: Vec<String> = part2.iter().map(|x| x.iter().collect::<String>()).collect();
    println!(
        "Part 2: {:?}",
        lines
            .iter()
            .map(|x| x.iter().collect::<String>())
            .collect::<Vec<_>>()
    );
    println!("Part 2: {:?}", (tow_pos + 1) * (six_pos + 1));
}

fn compare(left: &Packet, right: &Packet) -> Order {
    let left_is_list = is_list(left);
    let right_is_list = is_list(right);
    let mut result = Order::Equal;
    if left_is_list && right_is_list {
        let left = get_list(left);
        let right = get_list(right);
        result = compare(&left, &right);
    } else if !left_is_list && !right_is_list {
        let left_value = get_number(left);
        let right_value = get_number(right);
        if left_value.is_none() {
            if right_value.is_none() {
                return Order::Equal;
            }
            return Order::Right;
        } else if right_value.is_none() {
            return Order::Wrong;
        } else {
            let (left_value, left_index) = left_value.unwrap();
            let (right_value, right_index) = right_value.unwrap();
            if left_value == right_value {
                if left_index >= left.line.len() && right_index >= right.line.len() {
                    return Order::Equal;
                }
                return compare(
                    &Packet::new(left.line.clone(), left_index),
                    &Packet::new(right.line.clone(), right_index),
                );
            } else if left_value < right_value {
                return Order::Right;
            } else {
                return Order::Wrong;
            }
        }
    } else if left_is_list {
        if right.line.is_empty()
            || right.index >= right.line.len()
            || right.line[right.index] == ']'
        {
            return Order::Wrong;
        }
        result = compare(left, &create_list(right));
    } else if right_is_list {
        if left.line.is_empty() || left.index >= left.line.len() || left.line[left.index] == ']' {
            return Order::Right;
        }
        result = compare(&create_list(left), right);
    };
    if result != Order::Equal {
        return result;
    }
    let finished_left_list = get_list(left);
    let finished_right_list = get_list(right);
    compare(
        &Packet::new(
            left.line.clone(),
            left.index + finished_left_list.line.len() + 3,
        ),
        &Packet::new(
            right.line.clone(),
            right.index + finished_right_list.line.len() + 3,
        ),
    )
}

fn is_list(packet: &Packet) -> bool {
    packet.index < packet.line.len() && packet.line[packet.index] == '['
}

fn is_empty(packet: &Packet) -> bool {
    packet.index < packet.line.len() && packet.line[packet.index] == ']'
}

fn get_list(packet: &Packet) -> Packet {
    let line = &packet.line;
    let index = packet.index;
    if line.len() == 1 {
        return Packet::new(line.clone(), 0);
    }
    if line[index] != '[' {
        panic!("Invalid list");
    }
    let mut opened: usize = 0;
    let mut end: usize = 0;
    line.iter().enumerate().skip(index + 1).any(|(i, c)| {
        if *c == '[' {
            opened += 1;
        }
        if *c == ']' {
            if opened == 0 {
                end = i;
                return true;
            } else {
                opened -= 1;
            }
        }
        false
    });
    Packet::new(line[index + 1..end].to_vec(), 0)
}

fn create_list(packet: &Packet) -> Packet {
    let mut line = packet.line.clone();
    line.insert(packet.index, '[');
    if packet.index + 2 < line.len() && line[packet.index + 2] == '0' {
        line.insert(packet.index + 3, ']');
    } else {
        line.insert(packet.index + 2, ']');
    }
    Packet::new(line, packet.index)
}

fn get_number(packet: &Packet) -> Option<(usize, usize)> {
    if is_empty(packet) || is_list(packet) {
        return None;
    }
    let line = &packet.line;
    let index = packet.index;
    let mut end: usize = 0;
    line.iter().enumerate().skip(index).any(|(i, c)| {
        if *c == ',' || *c == ']' {
            end = i;
            return true;
        }
        false
    });
    if end == 0 {
        end = line.len();
    }
    if index >= end {
        return None;
    }
    Some((
        (line[index..end])
            .iter()
            .collect::<String>()
            .parse::<usize>()
            .unwrap(),
        end + 1,
    ))
}
