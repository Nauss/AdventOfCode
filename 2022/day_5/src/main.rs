use regex::Regex;
use std::collections::HashMap;

struct Instruction {
    count: i32,
    from: i32,
    to: i32,
}

fn get_crates() -> HashMap<i32, Vec<char>> {
    let mut crates = HashMap::new();
    crates.insert(1, vec!['F', 'C', 'J', 'P', 'H', 'T', 'W']);
    crates.insert(2, vec!['G', 'R', 'V', 'F', 'Z', 'J', 'B', 'H']);
    crates.insert(3, vec!['H', 'P', 'T', 'R']);
    crates.insert(4, vec!['Z', 'S', 'N', 'P', 'H', 'T']);
    crates.insert(5, vec!['N', 'V', 'F', 'Z', 'H', 'J', 'C', 'D']);
    crates.insert(6, vec!['P', 'M', 'G', 'F', 'W', 'D', 'Z']);
    crates.insert(7, vec!['M', 'V', 'Z', 'W', 'S', 'J', 'D', 'P']);
    crates.insert(8, vec!['N', 'D', 'S']);
    crates.insert(9, vec!['D', 'Z', 'S', 'F', 'M']);
    crates
}

fn move_crates(
    crates: &mut HashMap<i32, Vec<char>>,
    instruction: &Instruction,
    is_crate_mover9001: bool,
) {
    let mut removed = Vec::new();
    {
        let from = crates.get_mut(&instruction.from).unwrap();
        for _ in 0..instruction.count {
            removed.push(from.pop().unwrap());
        }
    }
    let to = crates.get_mut(&instruction.to).unwrap();
    if is_crate_mover9001 {
        removed.reverse();
    }
    for c in removed {
        to.push(c);
    }
}

fn main() {
    let re = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    let instructions = include_str!("../data.txt").lines().map(|line| {
        let caps = re.captures(line).unwrap();
        Instruction {
            count: caps[1].parse().unwrap(),
            from: caps[2].parse().unwrap(),
            to: caps[3].parse().unwrap(),
        }
    });

    let mut part1_crates = get_crates();
    let mut part2_crates = get_crates();

    instructions.for_each(|instruction| {
        move_crates(&mut part1_crates, &instruction, false);
        move_crates(&mut part2_crates, &instruction, true);
    });
    print!("part1: ");
    for key in 1..10 {
        print!("{}", part1_crates.get(&key).unwrap().last().unwrap());
    }
    println!("");

    print!("part2: ");
    for key in 1..10 {
        print!("{}", part2_crates.get(&key).unwrap().last().unwrap());
    }
    println!("");
}
