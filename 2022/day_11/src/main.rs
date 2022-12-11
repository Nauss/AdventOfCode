#[derive(Clone)]
struct Monkey {
    items: Vec<i64>,
    operation: fn(i64) -> i64,
    divider: i64,
    test: fn(i64) -> i64,
    inspected: i64,
}

fn main() {
    let mut monkeys = initial_monkeys();
    let common_divider: i64 = i64::MAX;

    for _ in 0..20 {
        for index in 0..monkeys.len() {
            monkeys = take_turn(monkeys, index, common_divider);
        }
    }
    monkeys.sort_by_key(|monkey| -monkey.inspected);
    println!(
        "Part 1: {}",
        monkeys
            .iter()
            .map(|monkey| monkey.inspected)
            .take(2)
            .product::<i64>()
    ); // 100345

    let mut monkeys = initial_monkeys();
    let common_divider: i64 = monkeys.iter().map(|monkey| monkey.divider).product();
    for _ in 0..10000 {
        for index in 0..monkeys.len() {
            monkeys = take_turn(monkeys, index, common_divider);
        }
    }
    monkeys.sort_by_key(|monkey| -monkey.inspected);
    println!(
        "Part 2: {}",
        monkeys
            .iter()
            .map(|monkey| monkey.inspected)
            .take(2)
            .product::<i64>()
    ); // 28537348205
}

fn take_turn(monkeys: Vec<Monkey>, index: usize, common_divider: i64) -> Vec<Monkey> {
    let mut result = monkeys;
    let mut monkey = result[index].clone();
    for item in &monkey.items {
        let mut level = (monkey.operation)(*item);
        if common_divider == i64::MAX {
            level = (level as f64 / 3.0).floor() as i64;
        }
        result[(monkey.test)(level) as usize]
            .items
            .push(level % common_divider);
    }
    monkey.inspected += monkey.items.len() as i64;
    monkey.items.clear();
    result[index] = monkey;
    result
}

fn initial_monkeys() -> Vec<Monkey> {
    vec![
        Monkey {
            items: vec![80],
            operation: |x| x * 5,
            divider: 2,
            test: |x| {
                if x % 2 == 0 {
                    4
                } else {
                    3
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![75, 83, 74],
            operation: |x| x + 7,
            divider: 7,
            test: |x| {
                if x % 7 == 0 {
                    5
                } else {
                    6
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![86, 67, 61, 96, 52, 63, 73],
            operation: |x| x + 5,
            divider: 3,
            test: |x| {
                if x % 3 == 0 {
                    7
                } else {
                    0
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![85, 83, 55, 85, 57, 70, 85, 52],
            operation: |x| x + 8,
            divider: 17,
            test: |x| {
                if x % 17 == 0 {
                    1
                } else {
                    5
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![67, 75, 91, 72, 89],
            operation: |x| x + 4,
            divider: 11,
            test: |x| {
                if x % 11 == 0 {
                    3
                } else {
                    1
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![66, 64, 68, 92, 68, 77],
            operation: |x| x * 2,
            divider: 19,
            test: |x| {
                if x % 19 == 0 {
                    6
                } else {
                    2
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![97, 94, 79, 88],
            operation: |x| x * x,
            divider: 5,
            test: |x| {
                if x % 5 == 0 {
                    2
                } else {
                    7
                }
            },
            inspected: 0,
        },
        Monkey {
            items: vec![77, 85],
            operation: |x| x + 6,
            divider: 13,
            test: |x| {
                if x % 13 == 0 {
                    4
                } else {
                    0
                }
            },
            inspected: 0,
        },
    ]
}
