using Pipe: @pipe
import Base.show
import Base.==
import Base.*
import Base.-
import Base.+

mutable struct Point
    x::Int
    y::Int
    z::Int
end

==(p1::Point, p2::Point) = p1.x == p2.x && p1.y == p2.y && p1.z == p2.z
===(p1::Point, p2::Point) = p1.x == p2.x && p1.y == p2.y && p1.z == p2.z
*(p1::Point, p2::Point) = Point(p1.x * p2.x, p1.y * p2.y, p1.z * p2.z)
+(p1::Point, p2::Point) = Point(p1.x + p2.x, p1.y + p2.y, p1.z + p2.z)
-(p1::Point, p2::Point) = Point(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)
function distance(p1::Point, p2::Point)
    Point(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
end

mutable struct Scanner
    name::String
    beacons::Array{Point}
    position::Union{Point,Nothing}
    rotation::Int   # index in the rotations array
end
Scanner(name::String, beacons::Array{Point}, position::Union{Point,Nothing}) = Scanner(name, beacons, position, -1)
Scanner(name::String, beacons::Array{Point}) = Scanner(name, beacons, nothing)

rotations = [
    ["x", " -z", " y"], ["x ", "-y ", "-z"], ["x", " z", " -y"], ["-x", " z", " y"], ["-x", " -y", " z"], ["-x", " -z", " -y"], ["-x", " y ", "-z"],
    ["z", "y", "-x"], ["-z", "y", "x"], ["-z", "-y", "-x"], ["z", "-y", "x"],
    ["y", "-x", "z"], ["-y", "x", "z"], ["y", "x", "-z"], ["-y", "-x", "-z"],
    ["-y", "z", "-x"], ["-y", "-z", "x"],
    ["y", "-z", "-x"], ["y", "z", "x"],
    ["z", "x", "y"], ["z", "-x", "-y"],
    ["-z", "-x", "y"], ["-z", "x", "-y"]]
origin = Point(0, 0, 0)

tostring(p::Point) = "x:" * string(p.x) * " y:" * string(p.y) * " z:" * string(p.z)
show(io::IO, p::Point) = show(io::IO, tostring(p))
function tostring(s::Scanner)
    result = ""
    result *= s.name
    result *= join(s.beacons, ", ")
    if s.position !== nothing
        result *= "position: " * tostring(s.position)
    end
    result
end
show(io::IO, s::Scanner) = show(io::IO, tostring(s))

function rotate(p::Point, index::Int)
    rotation = rotations[index]
    x = p.x
    y = p.y
    z = p.z
    if 'y' in rotation[1]
        x = p.y
    elseif 'z' in rotation[1]
        x = p.z
    end
    if '-' in rotation[1]
        x *= -1
    end
    if 'x' in rotation[2]
        y = p.x
    elseif 'z' in rotation[2]
        y = p.z
    end
    if '-' in rotation[2]
        y *= -1
    end
    if 'x' in rotation[3]
        z = p.x
    elseif 'y' in rotation[3]
        z = p.y
    end
    if '-' in rotation[3]
        z *= -1
    end
    Point(x, y, z)
end

all_rotations = Dict()
function rotate(s::Scanner, index::Int)
    if haskey(all_rotations, (s, index))
        return all_rotations[(s, index)]
    end
    result = Scanner(s.name * " r$index", [], s.position, index)
    for b in s.beacons
        push!(result.beacons, rotate(b, index))
    end
    all_rotations[(s, index)] = result
    result
end

function rotate(s::Scanner)
    result = []
    if s.rotation != -1
        push!(result, s)
        return result
    end
    for i = 1:length(rotations)
        push!(result, rotate(s, i))
    end
    result
end

function move(s::Scanner, p::Point)
    result = Scanner(s.name * " moved", [], p, s.rotation)
    for b in s.beacons
        push!(result.beacons, Point(
            b.x - p.x,
            b.y - p.y,
            b.z - p.z
        ))
    end
    result
end

function update!(s::Scanner, position::Point, rotation::Int)
    rotated = rotate(s, rotation)
    moved = move(rotated, position)
    s.beacons = []
    for b in moved.beacons
        push!(s.beacons, Point(
            b.x,
            b.y,
            b.z
        ))
    end
    s.position = position
    s.rotation = rotation
end

function match(s1::Scanner, s2::Scanner, p1::Point, p2::Point)
    d = distance(p1, p2)
    s2_moved = move(s2, d)
    matches = []
    for b1 in s1.beacons
        for b2 in s2_moved.beacons
            if distance(b2, b1) == origin
                push!(matches, b1)
                if length(matches) == 12
                    return matches
                end
            end
        end
    end
    matches
end

rawValues = @pipe "./data.txt" |> readlines;

scanners = []
current = nothing
for line in rawValues
    if startswith(line, "---")
        global current = Scanner("scanner " * string(length(scanners)), [], isempty(scanners) ? origin : nothing, -1)
    elseif line == ""
        push!(scanners, current)
        global current = nothing
    else
        values = @pipe split(line, ",") |> parse.(Int, _)
        push!(current.beacons, Point(values[1], values[2], values[3]))
    end
end
if current !== nothing
    push!(scanners, current)
end

beacons = []
scanned = [popat!(scanners, 1)]
push!(beacons, last(scanned).beacons...)
while !isempty(scanners)
    for current in scanned
        found = false
        for scanner_index = 1:length(scanners)
            tested_rotations = rotate(scanners[scanner_index])
            for tested in tested_rotations
                match_result = []
                found_position = 0
                move_distance = 0
                for refb in current.beacons
                    for testb in tested.beacons
                        match_result = match(current, tested, refb, testb)
                        if (length(match_result) >= 12)
                            found = true
                            found_position = distance(testb, refb)
                            move_distance = distance(refb, testb)
                            break
                        end
                    end
                    if found
                        break
                    end
                end
                if found
                    println("found: " * current.name * " -> " * tested.name)
                    #                     println("found $(length(match_result)) matches: " * current.name * " -> " * tested.name * ",
                    # position: ", found_position, " move_distance: ", move_distance)
                    # println(match_result)
                    next_scanned = popat!(scanners, scanner_index)
                    next_scanned.position = found_position

                    push!(scanned, move(tested, move_distance))
                    for beacon in last(scanned).beacons
                        if !(beacon in match_result) && !(beacon in beacons)
                            push!(beacons, beacon)
                        end
                    end
                    break
                end
            end
            if found
                break
            end
        end
        if found
            break
        end
    end
end

println("beacons ", beacons)
println("part1 ", length(beacons))

m_distance(p1::Point, p2::Point) = abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)
max_distance = 0
for s1 in scanned
    for s2 in scanned
        if s1 == s2
            continue
        end
        if m_distance(s1.position, s2.position) > max_distance
            global max_distance = m_distance(s1.position, s2.position)
        end
    end
end
println("max_distance ", max_distance)
