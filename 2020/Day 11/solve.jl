using Pipe: @pipe

data = @pipe "./data.txt" |> readlines |> split.(_, "");

nbrow = 95
nbcol = 93

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
# Default neighbours
EIGHT_NEIGHBOURS = [NORTH, NORTH .+ EAST, SOUTH, SOUTH .+ WEST, EAST, EAST .+ SOUTH, WEST, WEST .+ NORTH]

occupied(input, (r, c)) = begin
    if r < 1 || c < 1 || r > nbrow || c > nbcol return false end
    input[r][c] == "#"
end
free(input, (r, c)) = begin
    if r < 1 || c < 1 || r > nbrow || c > nbcol return false end
    input[r][c] == "L"
end

count(input) = begin
    count = 0
    for r=1:nbrow
        for c=1:nbcol
            if occupied(input, (r, c)) count += 1 end
        end
    end
    return count
end

count_neighbours(input, (r, c)) = begin
    count = 0
    for n in EIGHT_NEIGHBOURS
        if occupied(input, (r+ n[1], c + n[2])) count += 1 end
    end
    return count
end

current = deepcopy(data)
next = deepcopy(data)
while true
    changed = false
    for r=1:nbrow
        for c=1:nbcol
            nb = count_neighbours(current, (r,c))
            if current[r][c] == "L" && nb == 0       
                next[r][c] = "#"
                changed = true
            end
            if current[r][c] == "#" && nb >= 4      
                next[r][c] = "L"  
                changed = true
            end
        end
    end
    global current = deepcopy(next)
    if !changed break end
end

println("part1:", count(next))

count_neighbours2(input, (r, c)) = begin
    count = 0
    for n in EIGHT_NEIGHBOURS
        position = (r + n[1], c + n[2])
        while position[1] >= 0 && position[2] >= 0 && position[1] <= nbrow && position[2] <= nbcol
            if occupied(input, (position[1], position[2])) 
                count += 1
                break
            end
            if free(input, (position[1], position[2])) break end
            position = (position[1] + 1 * n[1], position[2] + 1 * n[2])
        end
    end
    return count
end

current = deepcopy(data)
next = deepcopy(data)
while true
    changed = false
    for r=1:nbrow
        for c=1:nbcol
            nb = count_neighbours2(current, (r,c))
            if current[r][c] == "L" && nb == 0       
                next[r][c] = "#"
                changed = true
            end
            if current[r][c] == "#" && nb >= 5      
                next[r][c] = "L"  
                changed = true
            end
        end
    end
    global current = deepcopy(next)
    if !changed break end
end

println("part2:", count(next))