using Pipe: @pipe

rawdata = @pipe "./data.txt" |> readlines

tilesize = 10
# imagesize = 3
imagesize = 12
directions = ["top", "left", "right", "bottom"]
flips = ["none", "h", "v"]
rotations = [0, 90, 180, 270]

tiles = Dict()
current_tile_number = 0
current_tile = Array{String}(undef, (tilesize, tilesize))
current_row = 1
for line in rawdata
    if startswith(line, "Tile")
        # Save the prvious tile
        if current_tile_number != 0
            # Create the tile
            tiles[current_tile_number] = current_tile
            # Clear the current tile
            global current_tile = Array{String}(undef, (tilesize, tilesize))
        end
        global current_tile_number = parse(Int, split(line)[2])
        global current_row = 1
    elseif !isempty(line)
        cols = split(line, "")
        for c = 1:tilesize
            global current_tile[current_row, c] = cols[c]
        end
        global current_row += 1
    end
end
# Last one
tiles[current_tile_number] = current_tile
# println("tiles: ", tiles)

opposite_direction(direction) = begin
    if direction == "top"
        return "bottom"
    elseif direction == "left"
        return "right"
    elseif direction == "right"
        return "left"
    elseif direction == "bottom"
        return "top"
    end
end

getdirection(x1, y1, x2, y2) = begin
    x = x2 - x1
    y = y2 - y1
    if x == 0
        if y > 0
            return "bottom"
        else
            return "top"
        end
    elseif x > 0
    end
end

getedge(tile, direction) = begin
    if direction == "top"
        return tile[1, :]
    elseif direction == "left"
        return tile[1:10]
    elseif direction == "right"
        return tile[:, 10]
    elseif direction == "bottom"
        return tile[10, :]
    end
end

flip(tile, direction) = begin
    if direction == "h"
        return tile[:, end:-1:1]
    elseif direction == "v"
        return tile[end:-1:1, :]
    else return tile
    end
end

rotate(tile, angle, size) = begin
    if angle == 90
        result = Array{String}(undef, (size, size))
        for x = 1:size
            result[x, :] = tile[end:-1:1, x]
        end
        return result
    elseif angle == 180
        return flip(flip(tile, "h"), "v")
    elseif angle == 270
        result = Array{String}(undef, (size, size))
        for x = 1:size
            result[size - x + 1, :] = tile[:, x]
        end
        return result
    else return tile
    end
end

isequal(edge1::Vector{String}, edge2::Vector{String}) = all(edge1 .== edge2)

# Check if tile2 fit along tile1 in the given position
# tile1 is fixed
# tile2 can be rotated/flipped
tilematch(tile1::Array{String,2}, tile2::Array{String,2}, direction) = begin    
    ref = getedge(tile1, direction)
    opposite = opposite_direction(direction)
    for r in rotations
        rotated = rotate(tile2, r, tilesize)
        for f in flips
            flipped = flip(rotated, f)
            if isequal(ref, getedge(flipped, opposite))
                return (flipped, r, f)
            end
        end
    end
end

next_image_rowcol(row, col) = begin
    if col + 1 > imagesize
        return (row + 1, 1)    
    end
    return (row, col + 1)
end

assemble(localtiles, image, row, col) = begin
    # Check if a tile would fit in the given location
    # println("localtiles: $(keys(localtiles))")
    # println("assembling($row, $col)")
    for tilepair in localtiles
        tile_number = tilepair[1]
        tile = tilepair[2]
        ok = true
        m = nothing
        # Check left
        if col > 1 && image[row, col - 1] != 0
            m = tilematch(image[row, col - 1], tile, "right")
            if isnothing(m)
                ok = false
            end
        end
        # Check right
        if ok && col < imagesize && image[row, col + 1] != 0
            tmp = tilematch(image[row, col + 1], tile, "left")
            if isnothing(tmp) || (!isnothing(m) && (tmp[2] != m[2] || tmp[3] != m[3]))
                ok = false
            end
            if ok && isnothing(m) m = tmp end
        end
        # Check top
        if ok && row > 1 && image[row - 1 , col] != 0
            tmp = tilematch(image[row - 1 , col], tile, "bottom")
            # if not found or rotated or flipped > not good
            if isnothing(tmp) || (!isnothing(m) && (tmp[2] != m[2] || tmp[3] != m[3]))
                ok = false
            end
            if ok && isnothing(m) m = tmp end
        end
        # Check bottom
        if ok && row < imagesize && image[row + 1 , col] != 0
            tmp = tilematch(image[row + 1 , col], tile, "top")
            # if not found or rotated or flipped > not good
            if isnothing(tmp) || (!isnothing(m) && (tmp[2] != m[2] || tmp[3] != m[3]))
                ok = false
            end
            if ok && isnothing(m) m = tmp end
        end
        if ok && !isnothing(m)
            # Validate tile
            image[row, col] = m[1]
            global result_tiles[row, col] = tile_number
            tilesrest = deepcopy(localtiles)
            delete!(tilesrest, tile_number)
            return assemble(tilesrest, image, next_image_rowcol(row, col)...)
        end
    end
end

result_tiles = Array{Any}(undef, (imagesize, imagesize))
solve() = begin
    image::Array{Any,2} = zeros(imagesize, imagesize)
    for tile in tiles
        for r in rotations
            rotated = rotate(tile[2], r, tilesize)
            for f in flips
                flipped = flip(rotated, f)
                image = zeros(imagesize, imagesize)
                image[1, 1] = flipped
                global result_tiles[1, 1] = tile[1]
                tilesrest = deepcopy(tiles)
                delete!(tilesrest, tile[1])
                assemble(tilesrest, image, next_image_rowcol(1, 1)...)
                if length(filter(x -> x == 0, image)) == 0
                    # Found
                    return image
                end
            end
        end
    end
    return image
end
image = solve()
println("part1: ", result_tiles[1, 1] * result_tiles[1, imagesize] * result_tiles[imagesize, 1] * result_tiles[imagesize, imagesize])

# Part 2
newtilesize = tilesize - 2
finalsize = imagesize * newtilesize
finalimage = Array{String}(undef, (finalsize, finalsize))
lineindex = 1
for r = 1:imagesize
    for tiler = 2:tilesize - 1
        for c = 1:imagesize
            tile = image[r,c]
            global finalimage[lineindex, 1 + (c - 1) * newtilesize:(c - 1) * newtilesize + newtilesize] = tile[tiler, 2:end - 1]
        end
        global lineindex += 1
    end
end

monster_top    = r"(..................)#(.)"
monster_middle = r"#(....)##(....)##(....)###"
monster_bottom = r"(.)#(..)#(..)#(..)#(..)#(..)#(...)"
monster_top_sub = s"\1O\2"
monster_middle_sub = s"O\1OO\2OO\3OOO"
monster_bottom_sub = s"\1O\2O\3O\4O\5O\6O\7"
nbmonsterpixels = 15
maxmonstersfound = 0
resultimage = finalimage
for r in rotations
    rotated = rotate(finalimage, r, finalsize)
    for f in flips
        flipped = flip(rotated, f)
        monstersfound = 0
        for index = 1:finalsize - 2
            line = join(flipped[index,:])
            line2 = join(flipped[index + 1,:])
            line3 = join(flipped[index + 2,:])
            searchindex = 1
            monsterindex = findnext(monster_top, line, searchindex)
            while monsterindex !== nothing
                if occursin(monster_middle, line2[monsterindex]) &&
                    occursin(monster_bottom, line3[monsterindex])
                    # Update flipped
                    flipped[index, monsterindex] = split(
                        replace(
                            join(flipped[index, monsterindex]),
                        monster_top => monster_top_sub
                    ), "")
                    flipped[index + 1, monsterindex] = split(
                        replace(
                            join(flipped[index + 1, monsterindex]),
                        monster_middle => monster_middle_sub
                    ), "")
                    flipped[index + 2, monsterindex] = split(
                        replace(
                            join(flipped[index + 2, monsterindex]),
                        monster_bottom => monster_bottom_sub
                    ), "")

                    monstersfound += 1
                    # Update lines
                    line = join(flipped[index,:])
                    line2 = join(flipped[index + 1,:])
                    line3 = join(flipped[index + 2,:])
                end
                searchindex += 1
                monsterindex = findnext(monster_top, line, searchindex)                
            end
        end
        if monstersfound > maxmonstersfound
            global resultimage = flipped
            global maxmonstersfound = monstersfound
        end
    end
end

roughness = 0
for r = 1:finalsize
    global roughness += count(x -> x == "#", resultimage[r,:])
end
println("part2: ", roughness)

todisp = []
for r = 1:finalsize
    push!(todisp, join(resultimage[r, :]))
end
# 2302
# 2407
# 2362
# 922
# 1072