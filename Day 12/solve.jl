using Pipe: @pipe

data = @pipe "./data.txt" |> readlines;

direction = 0
position = (0, 0)
inputs = []
for line in data
    push!(inputs, (line[1], parse(Int, line[2:end])))
end

for input in inputs
    if input[1] == 'N'
        global position = (position[1] - input[2], position[2])
    elseif input[1] == 'S'
        global position = (position[1] + input[2], position[2])
    elseif input[1] == 'E'
        global position = (position[1], position[2] + input[2])
    elseif input[1] == 'W'
        global position = (position[1], position[2] - input[2])
    elseif input[1] == 'L'
        global direction = (direction + input[2]) % 360
    elseif input[1] == 'R'
        global direction = (direction - input[2]) % 360
    elseif input[1] == 'F'
        if direction == 0 || direction == 360
            global position = (position[1], position[2] + input[2])
        elseif direction == 90 || direction == -270
            global position = (position[1] - input[2], position[2])
        elseif direction == 180 || direction == -180
            global position = (position[1], position[2] - input[2])
        elseif direction == 270 || direction == -90
            global position = (position[1] + input[2], position[2])
        else 
            println("direction error ", direction)
            break
        end
    end
end

println("part1:", abs(position[1]) + abs(position[2]))

waypoint = (-1, 10)
position = (0, 0)
inputs = []
for line in data
    push!(inputs, (line[1], parse(Int, line[2:end])))
end

for input in inputs
    if input[1] == 'N'
        global waypoint = (waypoint[1] - input[2], waypoint[2])
    elseif input[1] == 'S'
        global waypoint = (waypoint[1] + input[2], waypoint[2])
    elseif input[1] == 'E'
        global waypoint = (waypoint[1], waypoint[2] + input[2])
    elseif input[1] == 'W'
        global waypoint = (waypoint[1], waypoint[2] - input[2])
    elseif input[1] == 'L'
        x = waypoint[1]
        y = waypoint[2]
        angle = deg2rad(input[2])
        global waypoint = (cos(angle) * x - sin(angle) * y, sin(angle) * x + cos(angle) * y)
    elseif input[1] == 'R'
        x = waypoint[1]
        y = waypoint[2]
        angle = -deg2rad(input[2])
        global waypoint = (cos(angle) * x - sin(angle) * y, sin(angle) * x + cos(angle) * y)
    elseif input[1] == 'F'
        global position = (position[1] + input[2] * waypoint[1], position[2] + input[2] * waypoint[2])
    end
end

println("part1:", abs(position[1]) + abs(position[2]))