struct Node {
    value: usize,
    parent: Option<usize>,
    children: Vec<usize>,
}

impl Node {
    fn is_directory(&self) -> bool {
        self.children.len() > 0
    }
}

struct FileTree {
    files: Vec<Node>,
}

impl FileTree {
    fn insert(&mut self, value: usize, parent: Option<usize>) -> Option<usize> {
        let index = self.files.len();
        if let Some(parent) = parent {
            self.files[parent].children.push(index);
            self.update_size(Some(parent), value);
        }
        self.files.push(Node {
            value,
            parent,
            children: vec![],
        });
        Some(index)
    }

    fn node(&self, index: Option<usize>) -> &Node {
        match index {
            Some(index) => &self.files[index],
            None => panic!("Trying to access a non-existing node"),
        }
    }

    fn update_size(&mut self, index: Option<usize>, size: usize) {
        let mut current = index;
        while let Some(index) = current {
            let node = &mut self.files[index];
            node.value += size;
            current = node.parent;
        }
    }
}

const MAX_DIR_SIZE: usize = 100000;
const TOTAL_DISK_SIZE: usize = 70000000;
const UPDATE_SIZE: usize = 30000000;

fn main() {
    let mut file_tree = FileTree { files: vec![] };
    let mut current: Option<usize> = None;
    include_str!("../data.txt").lines().for_each(|line| {
        let splited: Vec<&str> = line.split(" ").collect();
        match splited[0] {
            "$" => match splited[1] {
                "cd" => match splited[2] {
                    ".." => {
                        current = file_tree.node(current).parent;
                    }
                    _ => {
                        current = file_tree.insert(0, current);
                    }
                },
                _ => {}
            },
            "dir" => {}
            _ => {
                file_tree.insert(splited[0].parse::<usize>().unwrap(), current);
            }
        }
    });
    let directories: Vec<&Node> = file_tree
        .files
        .iter()
        .filter(|node| node.is_directory())
        .collect();

    let part1: usize = directories
        .iter()
        .filter(|node| node.value <= MAX_DIR_SIZE)
        .map(|node| node.value)
        .sum();
    println!("part1 {}", part1);

    let to_delete_size = UPDATE_SIZE - (TOTAL_DISK_SIZE - file_tree.files[0].value);
    let part2 = directories
        .iter()
        .filter(|node| node.value >= to_delete_size)
        .map(|node| node.value)
        .min()
        .unwrap();
    println!("part2 {}", part2);
}
