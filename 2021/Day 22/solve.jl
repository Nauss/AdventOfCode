using Pipe: @pipe

struct Range
    action::String
    x1::Int
    x2::Int
    y1::Int
    y2::Int
    z1::Int
    z2::Int
end

volume(range::Range) = (range.x2 - range.x1) * (range.y2 - range.y1) * (range.z2 - range.z1)

line_regex = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"

rawValues = @pipe "./data.txt" |> readlines;

ranges = []
for line in rawValues
    m = match(line_regex, line)
    push!(ranges, Range(m.captures[1],
        parse(Int, m.captures[2]),
        parse(Int, m.captures[3]),
        parse(Int, m.captures[4]),
        parse(Int, m.captures[5]),
        parse(Int, m.captures[6]),
        parse(Int, m.captures[7]),
    ))
end

cubes = Dict()
for r in ranges
    for x in r.x1:r.x2
        for y in r.y1:r.y2
            for z in r.z1:r.z2
                if r.action == "on"
                    cubes[(x, y, z)] = true
                else
                    cubes[(x, y, z)] = false
                end
            end
        end
    end
end

part1 = 0
for cube in cubes
    if cube[2]
        global part1 += 1
    end
end
println("part1 ", part1)

cubes = 0
for r in 1:length(ranges)
    range = ranges[r]
    new_on = 0
    new_off = 0
    if range.action == "on"
        new_on = volume(range)
        # else
        #     new_off = (range.x2 - range.x1) * (range.y2 - range.y1) * (range.z2 - range.z1)
    end
    # Check overlaps
    for r2 in 1:r-1
        range2 = ranges[r2]
        if range2.action == "on"
            overlap = Range("on", max(range.x1, range2.x1), min(range.x2, range2.x2), max(range.y1, range2.y1), min(range.y2, range2.y2), max(range.z1, range2.z1), min(range.z2, range2.z2))
            if overlap.x2 >= overlap.x1 && overlap.y2 >= overlap.y1 && overlap.z2 >= overlap.z1
                new_on -= volume(overlap)
            end
        end
    end
    global cubes += new_on
    # global cubes -= new_off
end
println("cubes ", cubes)

