use std::collections::HashMap;

// 4 for part 1, 14 for part 2
const MARKER_LENGTH: usize = 14;

fn is_marker(sequence: &Vec<char>) -> bool {
    sequence
        .iter()
        .zip(sequence)
        .collect::<HashMap<_, _>>()
        .len()
        == MARKER_LENGTH
}

fn main() {
    let input = include_str!("../data.txt").chars();
    let mut sequence = Vec::new();
    for (index, c) in input.enumerate() {
        sequence.push(c);
        if sequence.len() > MARKER_LENGTH {
            sequence.remove(0);
        }
        if is_marker(&sequence) {
            println!("result: {}", index + 1);
            break;
        }
    }
}
