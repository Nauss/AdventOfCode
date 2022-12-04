fn main() {
    let ranges = include_str!("../data.txt").lines().map(|line| {
        let sections = line
            .split(",")
            .map(|sections| {
                sections
                    .split("-")
                    .map(|id| id.parse::<u32>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();
        (
            (sections[0][0]..(sections[0][1] + 1)),
            (sections[1][0]..(sections[1][1]) + 1),
        )
    });

    let part1 = ranges
        .clone()
        .filter(|(r1, r2)| {
            (r1.contains(&r2.start) && r1.contains(&(r2.end - 1)))
                || (r2.contains(&r1.start) && r2.contains(&(r1.end - 1)))
        })
        .count();

    let part2 = ranges
        .filter(|(r1, r2)| {
            (r1.contains(&r2.start) || r1.contains(&(r2.end - 1)))
                || (r2.contains(&r1.start) || r2.contains(&(r1.end - 1)))
        })
        .count();

    println!("part1 {}", part1);
    println!("part2 {}", part2);
}
