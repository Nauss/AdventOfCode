use std::collections::HashMap;

use regex::Regex;

#[derive(Debug, PartialEq, Hash, Eq, Clone, Copy)]
struct Position {
    x: isize,
    y: isize,
}

impl Position {
    fn new(x: isize, y: isize) -> Self {
        Self { x, y }
    }
}

#[derive(Debug)]
struct DataPoint {
    sensor: Position,
    beacon: Position,
}

impl DataPoint {
    fn new(sensor: Position, beacon: Position) -> Self {
        Self { sensor, beacon }
    }
    fn distance(&self) -> isize {
        self.sensor.x.abs_diff(self.beacon.x) as isize
            + (self.sensor.y.abs_diff(self.beacon.y)) as isize
    }
}

fn update_range(range: (Position, Position), position: Position) -> (Position, Position) {
    (
        Position::new(range.0.x.min(position.x), range.0.y.min(position.y)),
        Position::new(range.1.x.max(position.x), range.1.y.max(position.y)),
    )
}

fn main() {
    let re =
        Regex::new(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
            .unwrap();
    let data_points = include_str!("../data.txt")
        .lines()
        .map(|line| {
            let captures = re.captures(line).unwrap();
            let sensor = Position::new(
                captures.get(1).unwrap().as_str().parse().unwrap(),
                captures.get(2).unwrap().as_str().parse().unwrap(),
            );
            let beacon = Position::new(
                captures.get(3).unwrap().as_str().parse().unwrap(),
                captures.get(4).unwrap().as_str().parse().unwrap(),
            );
            DataPoint::new(sensor, beacon)
        })
        .collect::<Vec<DataPoint>>();

    let mut explored_range = (
        Position::new(isize::MAX, isize::MAX),
        Position::new(isize::MIN, isize::MIN),
    );
    // The locations map, for each position
    // true = a sensor or beacon is at that position
    // false = no sensor or beacon is at that position
    // if the position is not in the map, it is unknown
    let mut locations: HashMap<Position, bool> = HashMap::new();
    data_points.iter().for_each(|data_point| {
        locations.entry(data_point.sensor).or_insert(true);
        locations.entry(data_point.beacon).or_insert(true);

        explored_range = update_range(explored_range, data_point.sensor);
        explored_range = update_range(explored_range, data_point.beacon);

        // Set to false all the points within the beacon's range (from the sensor)
        let distance = data_point.distance();
        let x_range = data_point.sensor.x - distance..=data_point.sensor.x + distance;
        let y_range = data_point.sensor.y - distance..=data_point.sensor.y + distance;
        println!("x_range: {:?}", x_range);
        println!("y_range: {:?}", y_range);
        // for x in x_range {
        //     for y in y_range {
        //         let position = Position::new(x, y);
        //         locations.entry(position).or_insert(false);
        //     }
        // }
    });

    // println!("{:?}", locations);
    println!("explored_range: {:?}", explored_range);
}
