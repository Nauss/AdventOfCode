#[derive(Debug)]
enum Instruction {
    Noop,
    Addx(isize),
}

fn run(instruction: &Instruction, register: &mut Vec<isize>) {
    let &current = register.last().unwrap();
    match instruction {
        Instruction::Noop => register.push(current),
        Instruction::Addx(x) => {
            register.push(current);
            register.push(current + *x);
        }
    }
}

const SIZE: usize = 40;
fn main() {
    let mut register = vec![1];
    include_str!("../data.txt")
        .lines()
        .map(|line| {
            let mut splitted = line.split(' ');
            match splitted.next().unwrap() {
                "noop" => Instruction::Noop,
                "addx" => Instruction::Addx(splitted.next().unwrap().parse().unwrap()),
                _ => panic!("Unknown instruction"),
            }
        })
        .for_each(|instruction| run(&instruction, &mut register));
    let part1 = (20..221)
        .step_by(SIZE)
        .map(|i| (i as isize) * register[i - 1])
        .sum::<isize>();

    let mut screen: Vec<&str> = Vec::new();
    let mut sprite_position = 1; // middle of the sprite
    for (i, &x) in register[1..].iter().enumerate() {
        let pixel_position = (i % SIZE) as isize;
        if pixel_position.abs_diff(sprite_position) < 2 {
            screen.push("\u{2593}");
        } else {
            screen.push("\u{0020}");
        }
        sprite_position = x;
    }
    println!("Part 1: {}", part1);
    println!("Part 2:");
    (0..screen.len())
        .step_by(SIZE)
        .for_each(|i| println!("{}", screen[i..i + SIZE].join("")));
    println!(" ");
}
