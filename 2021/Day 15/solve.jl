using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "") |> hcat(_...) |> parse.(Int, _);

# Old method allowing only left and down
# grid_size = size(rawValues)
# start = (1, 1)
# exit = grid_size
# infinity = typemax(Int)
# flood = fill(infinity, grid_size)
# for x = 1:grid_size[1]
#     for y = 1:grid_size[2]
#         if x == 1 && y == 1
#             flood[x, y] = rawValues[x, y]
#             continue
#         end
#         # Get the lowset neighbour in rawValues
#         lowest = infinity
#         if x > 1 && flood[x-1, y] < lowest
#             lowest = flood[x-1, y]
#         end
#         if y > 1 && flood[x, y-1] < lowest
#             lowest = flood[x, y-1]
#         end
#         flood[x, y] = rawValues[x, y] + lowest
#     end
# end
mutable struct Node
    x::Int
    y::Int
    cost::Int
    h::Int
    parent::Union{Node,Nothing}
end
infinity = typemax(Int)
start = Node(1, 1, rawValues[1, 1], 0, nothing)
function get_neighbours(node)
    x = node.x
    y = node.y
    result = []
    if x > 1
        push!(result, Node(x - 1, y, 0, 0, nothing))
    end
    if y > 1
        push!(result, Node(x, y - 1, 0, 0, nothing))
    end
    if x < grid_size[1]
        push!(result, Node(x + 1, y, 0, 0, nothing))
    end
    if y < grid_size[2]
        push!(result, Node(x, y + 1, 0, 0, nothing))
    end
    return result
end
function compare(n1, n2)
    if n1.h < n2.h
        return 1
    elseif n1.h == n2.h
        return 0
    else
        return -1
    end
end
compare_position(n1, n2) = n1.x == n2.x && n1.y == n2.y
isin(node, list) = haskey(list, (node.x, node.y))
raw_cost(node, grid) = grid[node.x, node.y]
function cell_cost(node, list)
    index = findfirst(x -> compare_position(x, node), list)
    return list[index].cost
end
distance(node) = abs(node.x - exit.x) + abs(node.y - exit.y)
function get_smallest(list)
    smallest = infinity
    result = nothing
    for (key, node) in list
        if node.h < smallest
            smallest = node.h
            result = (key, (node))
        end
    end
    delete!(list, result[1])
    return result[2]
end

grid_size = size(rawValues)
exit = Node(grid_size[1], grid_size[2], rawValues[grid_size...], 0, nothing)
open_list = Dict((1, 1) => start)
closed_list = Dict()
last_node = Node(0, 0, 0, 0, nothing)
while !isempty(open_list)
    current = get_smallest(open_list)
    if compare_position(current, exit)
        global last_node = current
        break
    end
    for neighbour in get_neighbours(current)
        if !isin(neighbour, closed_list)
            cost = current.cost + raw_cost(neighbour, rawValues)
            if isin(neighbour, open_list) && cell_cost(neighbour, open_list) <= cost
                continue
            end
            neighbour.cost = cost
            neighbour.h = cost + distance(neighbour)
            neighbour.parent = current
            open_list[neighbour.x, neighbour.y] = neighbour
        end
    end
    closed_list[current.x, current.y] = current
end

part1 = 0
while last_node.parent !== nothing
    global part1 += raw_cost(last_node, rawValues)
    global last_node = last_node.parent
end
println("part1 ", part1)

full_map = []
for x = 1:5
    rows = []
    for y = 1:5
        sub_map = rawValues .+ (x + y - 2)
        map!(x -> x >= 10 ? x % 9 : x, sub_map, sub_map)
        if isempty(rows)
            rows = sub_map
        else
            rows = vcat(rows, sub_map)
        end
    end
    if isempty(full_map)
        global full_map = rows
    else
        global full_map = hcat(full_map, rows)
    end
end

grid_size = size(full_map)
exit = Node(grid_size[1], grid_size[2], full_map[grid_size...], 0, nothing)

open_list = Dict((1, 1) => start)
closed_list = Dict()
last_node = Node(0, 0, 0, 0, nothing)
while !isempty(open_list)
    current = get_smallest(open_list)
    if compare_position(current, exit)
        global last_node = current
        break
    end
    for neighbour in get_neighbours(current)
        if !isin(neighbour, closed_list)
            cost = current.cost + raw_cost(neighbour, full_map)
            if isin(neighbour, open_list) && cell_cost(neighbour, open_list) <= cost
                continue
            end
            neighbour.cost = cost
            neighbour.h = cost + distance(neighbour)
            neighbour.parent = current
            open_list[neighbour.x, neighbour.y] = neighbour
        end
    end
    closed_list[current.x, current.y] = current
end

part2 = 0
while last_node.parent !== nothing
    global part2 += raw_cost(last_node, full_map)
    global last_node = last_node.parent
end
println("part2 ", part2)