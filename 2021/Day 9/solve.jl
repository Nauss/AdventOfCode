using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "") |> hcat(_...) |> parse.(Int, _);
gridsize = size(rawValues)

function islocalmin(grid, x, y)
    value = grid[x, y]
    up = true
    if y > 1 && grid[x, y-1] <= value
        up = false
    end
    down = true
    if y < gridsize[2] && grid[x, y+1] <= value
        down = false
    end
    left = true
    if x > 1 && grid[x-1, y] <= value
        left = false
    end
    right = true
    if x < gridsize[1] && grid[x+1, y] <= value
        right = false
    end
    return up && down && left && right
end

mins = []
minpositions = []
for x = 1:gridsize[1]
    for y = 1:gridsize[2]
        # check neighbours
        if islocalmin(rawValues, x, y)
            # Keep the value
            push!(mins, rawValues[x, y])
            push!(minpositions, (x, y))
        end
    end
end

println("part1 ", sum(mins .+ 1))

function get_not_9(grid, position)
    list = []
    x = position[1]
    y = position[2]
    # Up
    if y > 1 && grid[x, y-1] < 9
        push!(list, (x, y - 1))
        grid[x, y-1] = 9
    end
    # Down
    if y < gridsize[2] && grid[x, y+1] < 9
        push!(list, (x, y + 1))
        grid[x, y+1] = 9
    end
    # Left
    if x > 1 && grid[x-1, y] < 9
        push!(list, (x - 1, y))
        grid[x-1, y] = 9
    end
    # Right
    if x < gridsize[1] && grid[x+1, y] < 9
        push!(list, (x + 1, y))
        grid[x+1, y] = 9
    end
    list
end

function basin_size(grid, startposition)
    list = get_not_9(grid, startposition)
    size = length(list)
    while length(list) > 0
        newlist = []
        for position in list
            append!(newlist, get_not_9(grid, position))
        end
        list = newlist
        size += length(list)
    end
    size
end

basins = []
for (x, y) in minpositions
    push!(basins, basin_size(rawValues, (x, y)))
end
sort!(basins, rev = true)
println("part2 ", basins[1] * basins[2] * basins[3])
