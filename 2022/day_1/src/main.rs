pub struct Elf {
    food: Vec<i32>,
}

fn total_calories(elf: &Elf) -> i32 {
    elf.food.iter().sum()
}

fn main() {
    let raw = include_str!("../data.txt");
    let lines = raw.lines();
    // Create an elf for each line block (separated by a newline)
    let mut elves: Vec<Elf> = Vec::new();
    let mut current_elf = Elf { food: Vec::new() };
    for line in lines {
        if line.is_empty() {
            elves.push(current_elf);
            current_elf = Elf { food: Vec::new() };
        } else {
            let calories = line.parse().unwrap();
            current_elf.food.push(calories);
        }
    }
    elves.push(current_elf);

    let part1 = elves.iter().map(|elf| total_calories(elf)).max().unwrap();
    println!("part1: {part1}");

    elves.sort_by(|elf1, elf2| total_calories(elf2).cmp(&total_calories(elf1)));
    let part2 = total_calories(&elves[0]) + total_calories(&elves[1]) + total_calories(&elves[2]);
    println!("part2: {part2}");
}
