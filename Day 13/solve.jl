using Pipe: @pipe

time = 1000303.0
data = @pipe "./data.txt" |> read(_, String) |> split(_, ",") |> filter(x -> x != "x", _) |> parse.(Int, _);

diffmin = typemax(Int32)
index = 1
for i = 1:length(data)
    v = ceil(time / data[i]) * data[i] - time
    if v < diffmin
        global diffmin = v
        global index = i
    end
end

println("part1:", data[index] * diffmin)

data2 = @pipe "./data.txt" |> read(_, String) |> split(_, ",");

departs = [[],[]]
for i = 1:length(data2)
    if data2[i] != "x" 
        push!(departs[1], i - 1)
        push!(departs[2], parse(Int, data2[i]))
    end
end

println("departs:", departs)
index = 2439024390240
found = false
time = 0
size = length(departs[2])
while true
    global time = index * departs[2][1]
    global found = true
    for i = 2:size
        # Check the rest
        nb = (time + departs[1][i]) / departs[2][i]
        if nb != ceil(nb)
            found = false
            break
        end
    end
    # println(index)
    if found break end
    if index % 1000000 == 0
        println(index)
    end
    # Advance index
    global index = index + 1
end
println("part2:", time)
