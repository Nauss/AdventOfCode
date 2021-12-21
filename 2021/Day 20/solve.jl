using Pipe: @pipe

# raw_enhancement = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
raw_enhancement = "#####.#.###.###.#.#.####.#####.####.#..####.##.####...##......#.##.##.#.#..#.##.###.#.#.#.##.#..#.####.#.#.##.#..........###.##...#.#...#.#.###..#...##.####.##...###.....##..##..##.#......#.#.##.#.#.##.#.......###.##.#.###.##..##.......##....#.##....#..###.######.##...##.##...#.#.##...##.##.#....##.####..#..#..##.##.#.#..#....#######.###.##...#.####..#.#.#.##...##..##.#.#.#.##.#.......###..######..###..##......###..###.#.#.#.......#.....##.#.##..#.##.#.##.####..#.##....##.#.#..#.####.##.#.#.##...#..##.####."
raw_enhancement = @pipe raw_enhancement |> replace.(_, "#" => "1") |> replace.(_, "." => "0")

rawValues = @pipe "./data.txt" |> readlines |> replace.(_, "#" => "1") |> replace.(_, "." => "0");
current_out_of_bounds = "0"

function get_neighbours(image, x, y)
    (x_min, y_min, x_max, y_max) = get_bounds(image, 0)
    result = ""
    for j in [y - 1, y, y + 1]
        for i in [x - 1, x, x + 1]
            inbounds = (i >= x_min && i <= x_max && j >= y_min && j <= y_max)
            if inbounds && haskey(image, (i, j))
                result *= string(image[(i, j)])
            else
                if inbounds
                    result *= "0"
                else
                    result *= current_out_of_bounds
                end
            end
        end
    end
    result
end

SEARCH_MARGIN = 1
function get_bounds(image, margin)
    x = @pipe keys(image) |> collect |> map(x -> x[1], _) |> sort
    y = @pipe keys(image) |> collect |> map(x -> x[2], _) |> sort
    (first(x) - margin, first(y) - margin, last(x) + margin, last(y) + margin)
end

function print_image(image)
    if length(image) == 0
        println("Empty")
        return
    end
    (x_min, y_min, x_max, y_max) = get_bounds(image, 0)
    println("Out of bounds: ", current_out_of_bounds)
    for y = y_min:y_max
        for x = x_min:x_max
            if haskey(image, (x, y)) && image[(x, y)] == '1'
                print("#")
            else
                print(".")
            end
        end
        println()
    end
end

function epoch(image)
    new_image = Dict()
    (x_min, y_min, x_max, y_max) = get_bounds(image, SEARCH_MARGIN)
    for x = x_min:x_max
        for y = y_min:y_max
            n = get_neighbours(image, x, y)
            position = parse(Int, n, base = 2)
            new_value = raw_enhancement[position+1]
            if new_value == '1'
                new_image[(x, y)] = '1'
            end
        end
    end
    if current_out_of_bounds == "0"
        global current_out_of_bounds = "1"
    else
        global current_out_of_bounds = "0"
    end
    new_image
end

image = Dict()
x = 0
y = 0
for line in rawValues
    for char in line
        if char == '1'
            global image[(x, y)] = char
        end
        global x = x + 1
    end
    global y = y + 1
    global x = 0
end

result = epoch(image)
println("first result")
print_image(result)
result = epoch(result)
println("second result")
print_image(result)
println("part1 ", length(result))

for i = 1:50
    println("epoch ", i)
    global image = epoch(image)
end
println("part2 ", length(image))


