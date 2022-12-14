use std::cmp::Ordering;
use std::cmp::Ordering::{Equal, Greater, Less};

#[derive(Debug, Clone)]
struct Packet {
    line: String,
    starts: Vec<usize>,
    ends: Vec<usize>,
    index: usize,
}

impl Packet {
    fn new(line: String) -> Self {
        let mut starts = Vec::new();
        let mut ends = Vec::new();
        for (i, c) in line.chars().enumerate() {
            match c {
                '[' => starts.push(i),
                ']' => ends.push(i),
                _ => (),
            }
        }
        Packet {
            line,
            starts,
            ends,
            index: 0,
        }
    }
    fn is_list(&self) -> bool {
        self.starts.contains(&self.index)
    }
    fn is_end(&self) -> bool {
        self.ends.contains(&self.index)
    }
    fn is_last(&self) -> bool {
        self.index == self.line.len() - 1
    }
}

#[derive(Debug)]
struct Packets {
    left: Packet,
    right: Packet,
}

impl Packets {
    fn new(left: Packet, right: Packet) -> Self {
        Packets { left, right }
    }
}

const SKIP: [char; 2] = [']', ','];

fn main() {
    let lines = include_str!("../data.txt").lines().collect::<Vec<_>>();
    let mut packets = Vec::new();
    for i in (0..lines.len()).step_by(3) {
        packets.push(Packets::new(
            Packet::new(lines[i].to_string()),
            Packet::new(lines[i + 1].to_string()),
        ));
    }
    // println!("Hello, world! {:?}", packets);

    let ordered: Vec<Ordering> = packets.iter().map(is_ordered).collect();
    let part1 = ordered.iter().enumerate().fold(0, |acc, (i, o)| {
        if *o == Less {
            return acc + (i + 1);
        }
        acc
    });
    println!("order: {:?}", ordered);
    println!("Part 1 {}", part1); // 6299 too high, 5840 too high, 5839 too high
}

fn is_ordered(packets: &Packets) -> Ordering {
    let left_is_list = packets.left.is_list();
    let right_is_list = packets.right.is_list();
    match (left_is_list, right_is_list) {
        (true, true) => {
            let mut left = packets.left.clone();
            left.index += 1;
            let mut right = packets.right.clone();
            right.index += 1;
            is_ordered(&Packets::new(left, right))
        }
        (true, false) => {
            if packets.right.is_end() {
                return Greater;
            }
            let mut right = packets.right.clone();
            right.line = format!(
                "{}[{}]{}",
                &right.line[..packets.right.index],
                &right.line[packets.right.index..packets.right.index + 1],
                &right.line[packets.right.index + 1..]
            );
            right.starts.push(packets.right.index);
            right.ends.push(packets.right.index + 2);
            is_ordered(&Packets::new(packets.left.clone(), right))
        }
        (false, true) => {
            if packets.left.is_end() {
                return Less;
            }
            let mut left = packets.left.clone();
            left.line = format!(
                "{}[{}]{}",
                &left.line[..packets.left.index],
                &left.line[packets.left.index..packets.left.index + 1],
                &left.line[packets.left.index + 1..]
            );
            left.starts.push(packets.left.index);
            left.ends.push(packets.left.index + 2);
            is_ordered(&Packets::new(left, packets.right.clone()))
        }
        (false, false) => {
            let c_left = packets.left.line.chars().nth(packets.left.index);
            if c_left.is_none() {
                return Less;
            }
            let c_left = c_left.unwrap();
            let c_right = packets.right.line.chars().nth(packets.right.index);
            if c_right.is_none() {
                return Greater;
            }
            let c_right = c_right.unwrap();

            let result = c_left.cmp(&c_right);

            if result != Equal {
                if c_left == ']' {
                    // if c_left == ']' && packets.left.is_last() {
                    return Less;
                }
                if c_right == ']' {
                    // if c_right == ']' && packets.right.is_last() {
                    return Greater;
                }
            }

            match result {
                Equal => {
                    let mut left = packets.left.clone();
                    left.index += 1;
                    while left.index < left.line.len()
                        && SKIP.contains(&left.line.chars().nth(left.index).unwrap())
                    {
                        left.index += 1;
                    }
                    if left.index == left.line.len() {
                        return Less;
                    }
                    let mut right = packets.right.clone();
                    right.index += 1;
                    while right.index < right.line.len()
                        && SKIP.contains(&right.line.chars().nth(right.index).unwrap())
                    {
                        right.index += 1;
                    }
                    if right.index == right.line.len() {
                        return Greater;
                    }
                    is_ordered(&Packets::new(left, right))
                }
                _ => result,
            }
        }
    }
}
