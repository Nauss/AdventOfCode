#[derive(Clone, Copy)]
enum Choice {
    Rock = 1,
    Paper,
    Scissors,
}

fn main() {
    let mut part1 = 0;
    let mut part2 = 0;
    include_str!("../data.txt")
        .lines()
        .map(|line| line.split(' ').collect::<Vec<&str>>())
        .for_each(|choices| {
            let opponent = get_choice(&choices[0]);
            part1 += game(&opponent, &get_choice(&choices[1]));
            part2 += game(&opponent, &get_strategy(&opponent, &choices[1]));
        });
    println!("part1: {part1}");
    println!("part2: {part2}");
}

fn game(opponent: &Choice, me: &Choice) -> i32 {
    let item_score = *me as i32;
    let result = match (opponent, me) {
        (Choice::Rock, Choice::Paper) => 6,
        (Choice::Rock, Choice::Scissors) => 0,
        (Choice::Paper, Choice::Rock) => 0,
        (Choice::Paper, Choice::Scissors) => 6,
        (Choice::Scissors, Choice::Rock) => 6,
        (Choice::Scissors, Choice::Paper) => 0,
        _ => 3,
    };
    result + item_score
}

fn get_choice(strategy: &str) -> Choice {
    match strategy {
        "A" => Choice::Rock,
        "B" => Choice::Paper,
        "C" => Choice::Scissors,
        "X" => Choice::Rock,
        "Y" => Choice::Paper,
        "Z" => Choice::Scissors,
        _ => panic!("Invalid strategy"),
    }
}

fn get_strategy(opponent: &Choice, me: &str) -> Choice {
    match me {
        "X" => lose(opponent),
        "Y" => opponent.clone(),
        "Z" => win(opponent),
        _ => panic!("Invalid strategy"),
    }
}

fn win(choice: &Choice) -> Choice {
    match choice {
        Choice::Rock => Choice::Paper,
        Choice::Paper => Choice::Scissors,
        Choice::Scissors => Choice::Rock,
    }
}

fn lose(choice: &Choice) -> Choice {
    match choice {
        Choice::Rock => Choice::Scissors,
        Choice::Paper => Choice::Rock,
        Choice::Scissors => Choice::Paper,
    }
}
