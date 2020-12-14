using Pipe: @pipe

data = @pipe "./data.txt" |> readlines |> parse.(Int, _) |> sort;

count1 = 1  # The step between the outlet and the first adapter
count3 = 1  # device's built-in adapter is always 3 higher

for i = 2:length(data)
    if data[i] - data[i - 1] == 1 global count1 += 1 end
    if data[i] - data[i - 1] == 3 global count3 += 1 end
end
println("part1: ", count1 * count3)

count = 0
tree = Dict(0 => 1)
for index = 1:length(data)
    newtree = Dict()
    for value in tree
        for i = 0:length(data)
            if index + i > length(data) break end
            d = data[index + i]
            if d > value[1] &&  d - value[1] <= 3
                if haskey(newtree, d)
                    newtree[d] += value[2]
                else
                    newtree[d] = value[2]
                end
                if index + i == length(data)
                    # Found a leaf
                    global count += value[2]
                end
            end
        end
    end
    global tree = newtree
end

println("count:", count)
