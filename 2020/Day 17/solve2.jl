using Pipe: @pipe

rawdata = @pipe "./data.txt" |> readlines |> split.(_, "");
grid = Dict()
for y = 1:length(rawdata)
    line = rawdata[y]
    for x = 1:length(line)
        global grid[(x, y, 0, 0)] = line[x] == "#"
    end
end
xrange = (0, length(rawdata[1]) + 1)
yrange = (0, length(rawdata) + 1)
zrange = (-1, 1)
wrange = (-1, 1)
check_neighbours(grid, cell) = begin
    active = 0
    count = 0
    for x = -1:1    
        for y = -1:1    
            for z = -1:1
                for w = -1:1
                    if x == 0 && y == 0 && z == 0 && w == 0 continue end
                    key = (x + cell[1], y + cell[2], z + cell[3], w + cell[4])
                    if haskey(grid, key) && grid[key] active += 1 end
                end
            end
        end
    end
    return active
end

for i = 1:6
    current = deepcopy(grid)
    for x = xrange[1]:xrange[2]
        for y = yrange[1]:yrange[2]
            for z = zrange[1]:zrange[2]
                for w = wrange[1]:wrange[2]
                    cell = (x, y, z, w)
                    active = check_neighbours(grid, cell)
                    if haskey(grid, cell)
                        if grid[cell]
                            if active == 2 || active == 3
                                current[cell] = true
                            else
                                current[cell] = false
                            end
                        elseif !grid[cell]
                            if active == 3
                                current[cell] = true
                            else
                                current[cell] = false
                            end
                        end
                    else
                        if active == 3
                            current[cell] = true
                        else
                            current[cell] = false
                        end
                    end
                end
            end
        end
    end
    global grid = deepcopy(current)
    # Update ranges
    global xrange = (xrange[1] - 1, xrange[2] + 1)
    global yrange = (yrange[1] - 1, yrange[2] + 1)
    global zrange = (zrange[1] - 1, zrange[2] + 1)
    global wrange = (wrange[1] - 1, wrange[2] + 1)
end

println("part1:",count(x -> x[2], grid))
