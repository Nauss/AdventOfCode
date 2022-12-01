pub struct Elf {
    food: Vec<i32>,
}

impl Elf {
    pub fn new() -> Elf {
        Elf { food: Vec::new() }
    }

    pub fn total_calories(&self) -> i32 {
        self.food.iter().sum()
    }
}

fn main() {
    let lines = include_str!("../data.txt").lines();
    // Create an elf for each line block (separated by a newline)
    let mut elves: Vec<Elf> = Vec::new();
    let mut current_elf = Elf::new();
    for line in lines {
        if line.is_empty() {
            elves.push(current_elf);
            current_elf = Elf::new();
        } else {
            let calories = line.parse().unwrap();
            current_elf.food.push(calories);
        }
    }
    elves.push(current_elf);

    elves.sort_by(|elf1, elf2| elf2.total_calories().cmp(&elf1.total_calories()));
    let part1 = elves[0].total_calories();
    println!("part1: {part1}");

    let part2: i32 = elves[0..3].iter().map(|elf| elf.total_calories()).sum();
    println!("part2: {part2}");
}
