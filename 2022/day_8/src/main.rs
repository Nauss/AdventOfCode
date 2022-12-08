use grid::*;

const INPUT_SIZE: usize = 99;
fn main() {
    let raw_data = include_str!("../data.txt")
        .chars()
        .filter(|c| !c.is_whitespace())
        .map(|c| c.to_digit(10).unwrap() as isize)
        .collect::<Vec<_>>();
    let input = Grid::from_vec(raw_data, INPUT_SIZE);

    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}

fn part2(input: &Grid<isize>) -> i32 {
    let mut output: Grid<i32> = Grid::new(INPUT_SIZE, INPUT_SIZE);
    for row in 0..input.rows() {
        for col in 0..input.cols() {
            let height = input.get(row, col).unwrap();
            // To right
            let mut to_right = 0;
            if col < input.cols() - 1 {
                for c in (col + 1)..input.cols() {
                    let h = input.get(row, c).unwrap();
                    to_right += 1;
                    if *h >= *height {
                        break;
                    }
                }
            }
            // To left
            let mut to_left = 0;
            if col > 0 {
                for c in (0..col).rev() {
                    let h = input.get(row, c).unwrap();
                    to_left += 1;
                    if *h >= *height {
                        break;
                    }
                }
            }
            // To bottom
            let mut to_bottom = 0;
            if row < input.rows() - 1 {
                for r in (row + 1)..input.rows() {
                    let h = input.get(r, col).unwrap();
                    to_bottom += 1;
                    if *h >= *height {
                        break;
                    }
                }
            }
            // To top
            let mut to_top = 0;
            if row > 0 {
                for r in (0..row).rev() {
                    let h = input.get(r, col).unwrap();
                    to_top += 1;
                    if *h >= *height {
                        break;
                    }
                }
            }
            output[row][col] = to_right * to_left * to_bottom * to_top;
        }
    }
    *output.iter().max().unwrap()
}

fn part1(input: &Grid<isize>) -> i32 {
    let mut output: Grid<i32> = Grid::new(INPUT_SIZE, INPUT_SIZE);
    // Left to right
    for row in 0..input.rows() {
        let mut current_height: isize = -1;
        for col in 0..input.cols() {
            let height = input.get(row, col).unwrap();
            if *height > current_height {
                output[row][col] = 1;
                current_height = *height;
            }
            if current_height == 9 {
                break;
            }
        }
    }
    // Right to left
    for row in 0..input.rows() {
        let mut current_height: isize = -1;
        for col in (0..input.cols()).rev() {
            let height = input.get(row, col).unwrap();
            if *height > current_height {
                output[row][col] = 1;
                current_height = *height;
            }
            if current_height == 9 {
                break;
            }
        }
    }
    // Top to bottom
    for col in 0..input.cols() {
        let mut current_height: isize = -1;
        for row in 0..input.rows() {
            let height = input.get(row, col).unwrap();
            if *height > current_height {
                output[row][col] = 1;
                current_height = *height;
            }
            if current_height == 9 {
                break;
            }
        }
    }
    // Bottom to top
    for col in 0..input.cols() {
        let mut current_height: isize = -1;
        for row in (0..input.rows()).rev() {
            let height = input.get(row, col).unwrap();
            if *height > current_height {
                output[row][col] = 1;
                current_height = *height;
            }
            if current_height == 9 {
                break;
            }
        }
    }
    output.iter().sum::<i32>()
}
