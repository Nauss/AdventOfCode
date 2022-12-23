use std::collections::{HashMap, HashSet};

use regex::Regex;

#[derive(Debug, Clone)]
struct Valve {
    name: String,
    flow: u32,
    tunnels: Vec<String>,
}

impl Valve {
    fn new(name: String, flow: u32, tunnels: Vec<String>) -> Self {
        Self {
            name,
            flow,
            tunnels,
        }
    }
}

const STARTING_VALVE: &str = "AA";
const ERUPTION_TIME: u32 = 30;

fn sorted_working_valves(valves: &Vec<Valve>) -> Vec<String> {
    let working_valves = valves
        .iter()
        .filter(|v| v.flow > 0)
        .map(|v| v.name.to_string())
        .collect::<Vec<String>>();
    working_valves
}

fn get_path_to(visited: &mut HashSet<String>, valves: &Vec<Valve>, to: &String) -> Vec<String> {
    let mut found = valves
        .iter()
        .filter_map(|v| {
            if !visited.contains(&v.name) && v.tunnels.contains(to) {
                let found_name = v.name.to_string();
                let mut result = vec![];
                result.push(found_name.clone());
                if found_name != STARTING_VALVE {
                    result.extend(get_path_to(visited, valves, &found_name))
                }
                return Some(result);
            }
            None
        })
        .collect::<Vec<_>>();
    found.sort_by_key(|v| v.len());
    found[0].clone()
}

fn main() {
    let re = Regex::new(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
        .unwrap();

    let mut valves: Vec<Valve> = include_str!("../data.txt")
        .lines()
        .map(|line| {
            let caps = re.captures(line).unwrap();
            let name = caps.get(1).unwrap().as_str();
            let flow = caps.get(2).unwrap().as_str().parse::<u32>().unwrap();
            let tunnels = caps
                .get(3)
                .unwrap()
                .as_str()
                .split(", ")
                .map(|s| s.to_string())
                .collect();
            Valve::new(name.to_string(), flow, tunnels)
        })
        .collect();
    valves.sort_by_key(|v| v.flow);
    valves.reverse();
    println!("Part 1: {:?}", valves);

    let goals = sorted_working_valves(&valves);
    println!("goals: {:?}", goals);
    let paths_to = goals
        .iter()
        .map(|g| {
            println!("searching for path to {}", g);
            let mut visited = HashSet::new();
            get_path_to(&mut visited, &valves, &g.clone())
        })
        .collect::<Vec<_>>();
    println!("paths_to: {:?}", paths_to);
}
// let mut part1 = 0;
// let mut current_valve = vec![String::from("AA")];
// let mut flow_rate = 0;
// for _ in 1..=ERUPTION_TIME {
//     let mut valve = valves.get(current_valve.last().unwrap()).unwrap().clone();
//     if valve.flow > 0 {
//         // Open the valve
//         flow_rate += valve.flow;
//         valve.flow = 0;
//     } else {
//         // Go to the next tunnel
//         let next = valve.tunnels.remove(0);
//         current_valve.push(next);
//     }

//     part1 += flow_rate;
//     valves.insert(valve.name.clone(), valve);
// }
