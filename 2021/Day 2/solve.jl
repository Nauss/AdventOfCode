using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, " ");

horizontal = 0;
depth = 0;
for value in rawValues
    direction = value[1]
    distance = parse(Int, value[2])
    if direction == "forward"
        global horizontal += distance
    elseif direction == "down"
        global depth += distance
    elseif direction == "up"
        global depth -= distance
    end
end
println("part1 ", horizontal * depth)

horizontal = 0;
depth = 0;
aim = 0;
for value in rawValues
    direction = value[1]
    distance = parse(Int, value[2])
    if direction == "forward"
        global horizontal += distance
        global depth += distance * aim
    elseif direction == "down"
        global aim += distance
    elseif direction == "up"
        global aim -= distance
    end
end

println("part2 ", horizontal * depth)
