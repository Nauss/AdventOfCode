use std::collections::HashMap;

fn main() {
    let content = include_str!("../data.txt");
    let part1: u32 = content.lines().map(|line| priority(in_both(line))).sum();
    let part2: u32 = content
        .lines()
        .map(|line| {
            let mut sorted: Vec<char> = line.chars().collect();
            sorted.sort_unstable();
            sorted.dedup();
            sorted
        })
        .collect::<Vec<Vec<char>>>()
        .chunks(3)
        .map(|group| {
            let mut counts = HashMap::new();
            let mut found: Option<char> = None;
            for c in group.concat().iter() {
                if *counts.entry(c).and_modify(|c| *c += 1).or_insert(1) == 3 {
                    found = Some(*c);
                    break;
                }
            }
            priority(found.unwrap())
        })
        .sum();
    println!("part1 {part1}");
    println!("part2 {part2}");
}

fn in_both(items: &str) -> char {
    // Split the items in two halves
    let (left, right) = items.split_at(items.len() / 2);
    // Extract the only common character
    left.chars().find(|&c| right.contains(c)).unwrap()
}

fn priority(c: char) -> u32 {
    if c.is_ascii_lowercase() {
        c as u32 - 96
    } else {
        c as u32 - 64 + 26
    }
}
