use std::collections::HashSet;

type Position = (i32, i32);

fn main() {
    let mut lowest = 0;
    let lines = include_str!("../data.txt")
        .lines()
        .map(|line| {
            line.split(" -> ")
                .map(|position| {
                    let mut position = position.split(',').map(|x| x.parse::<i32>().unwrap());
                    let x = position.next().unwrap();
                    let y = position.next().unwrap();
                    lowest = lowest.max(y);
                    (x, y)
                })
                .collect::<Vec<Position>>()
        })
        .collect::<Vec<_>>();

    println!("Lowest: {}", lowest);

    let mut terrain = HashSet::new();
    for line in &lines {
        // Iterate over the positions 2 by 2
        for pair in line.windows(2) {
            let (x1, y1) = pair[0];
            let (x2, y2) = pair[1];
            // Iterate over the positions between the 2
            for x in x1.min(x2)..=x1.max(x2) {
                for y in y1.min(y2)..=y1.max(y2) {
                    terrain.insert((x, y));
                }
            }
        }
    }
    let mut part1 = 0;
    loop {
        let done = move_sand(&mut terrain, (500, 0), lowest);
        if done {
            break;
        }
        part1 += 1;
    }
    println!("Part 1 {:?}", part1);

    let mut part2 = 0;
    loop {
        let done = move_sand2(&mut terrain, (500, 0), lowest);
        part2 += 1;
        if done {
            break;
        }
    }
    println!("Part 2 {:?}", part1 + part2);
}

fn move_sand(terrain: &mut HashSet<(i32, i32)>, position: Position, lowest: i32) -> bool {
    let (x, y) = position;
    if y > lowest {
        return true;
    }
    if terrain.contains(&(x, y + 1)) {
        // try on left
        if terrain.contains(&(x - 1, y + 1)) {
            // try on right
            if terrain.contains(&(x + 1, y + 1)) {
                // stop
                terrain.insert((x, y));
                false
            } else {
                // move right
                move_sand(terrain, (x + 1, y + 1), lowest)
            }
        } else {
            move_sand(terrain, (x - 1, y + 1), lowest)
        }
    } else {
        move_sand(terrain, (x, y + 1), lowest)
    }
}

fn move_sand2(terrain: &mut HashSet<(i32, i32)>, position: Position, lowest: i32) -> bool {
    let (x, y) = position;
    if y == lowest + 1 || terrain.contains(&(x, y + 1)) {
        // try on left
        if y == lowest + 1 || terrain.contains(&(x - 1, y + 1)) {
            // try on right
            if y == lowest + 1 || terrain.contains(&(x + 1, y + 1)) {
                // stop
                if x == 500 && y == 0 {
                    return true;
                }
                terrain.insert((x, y));
                false
            } else {
                // move right
                move_sand2(terrain, (x + 1, y + 1), lowest)
            }
        } else {
            move_sand2(terrain, (x - 1, y + 1), lowest)
        }
    } else {
        move_sand2(terrain, (x, y + 1), lowest)
    }
}
