using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "-");

connections = []
for line in rawValues
    (from, to) = line
    push!(connections, (from, to))
end

isbig(x) = isuppercase(x[1])
issmall(x) = islowercase(x[1])
function get_connected(x)
    connected = []
    for (from, to) in connections
        if (from == x)
            push!(connected, to)
        elseif (to == x)
            push!(connected, from)
        end
    end
    connected
end
can_visit(path, x) = !(x in path) || isbig(x)

paths = []
function part1(current, path)
    push!(path, current)
    connected = get_connected(current)
    for c in connected
        newPath = copy(path)
        if c == "end"
            # Found a path
            push!(newPath, c)
            push!(paths, newPath)
        else
            if can_visit(path, c)
                part1(c, newPath)
            end
        end
    end
end

part1("start", [])
println("part1 ", length(paths))

visited_twice(path) = !allunique(filter(x -> issmall(x), path))
function different_small_twice(path)
    result = Dict()
    for p in path
        if issmall(p)
            if haskey(result, p)
                result[p] += 1
            else
                result[p] = 1
            end
        end
    end
    count(p -> p.second == 2, collect(result)) > 1
end

function can_visit2(path, x)
    if isbig(x)
        return true
    end
    if x == "start" || x == "end"
        return false
    end
    count(c -> c == x, path) <= 1
end

paths = Set()
function part2(current, path,)
    if !isempty(path) && last(path) == current
        return
    end
    push!(path, current)
    if different_small_twice(path)
        return
    end
    connected = get_connected(current)
    for c in connected
        newPath = copy(path)
        if c == "end"
            # Found a path
            push!(newPath, c)
            push!(paths, newPath)
        else
            if can_visit2(path, c)
                part2(c, newPath)
            end
        end
    end
end

part2("start", [])

println("part2 ", length(filter(path -> !different_small_twice(path), paths)))
