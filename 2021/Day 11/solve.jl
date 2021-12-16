using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "") |> hcat(_...) |> parse.(Int, _);
gridsize = (10, 10);

flashes = 0

function update_neighbors!(values, x, y)
    # Up
    if y > 1
        values[x, y-1] += 1
        # Up left
        if x > 1
            values[x-1, y-1] += 1
        end
        # Up right
        if x < gridsize[1]
            values[x+1, y-1] += 1
        end
    end
    # Down
    if y < gridsize[2]
        values[x, y+1] += 1
        # Down left
        if x > 1
            values[x-1, y+1] += 1
        end
        # Down right
        if x < gridsize[1]
            values[x+1, y+1] += 1
        end
    end
    # Left
    if x > 1
        values[x-1, y] += 1
    end
    # Right
    if x < gridsize[1]
        values[x+1, y] += 1
    end
end

function flash!(values)
    x = 1
    y = 1
    while true
        if values[x, y] > 9
            values[x, y] = -1000
            global flashes += 1
            update_neighbors!(values, x, y)
            x = 1
            y = 1
        else
            y += 1
            if y > gridsize[2]
                x += 1
                if x > gridsize[1]
                    break
                end
                y = 1
            end
        end
    end
    for x = 1:gridsize[1]
        for y = 1:gridsize[2]
            if values[x, y] < 0
                values[x, y] = 0
            end
        end
    end
end

step!(values) = values .+= 1;

for i = 1:100
    step!(rawValues)
    flash!(rawValues)
end

println("part1 ", flashes)

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "") |> hcat(_...) |> parse.(Int, _);

step = 1
while true
    global flashes = 0
    step!(rawValues)
    flash!(rawValues)
    if flashes == gridsize[1] * gridsize[2]
        break
    end
    global step += 1
end
println("part2 ", step)
