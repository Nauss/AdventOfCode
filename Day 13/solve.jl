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

starts = []
ids = []
for i = 1:length(data2)
    if data2[i] != "x" 
        push!(starts, i - 1)
        push!(ids, parse(Int, data2[i]))
    end
end

found = false
time = 0
size = length(starts)
increment = 1
idsindex = 1
while idsindex <= length(ids)
    global found = true
    if (time + starts[idsindex]) % ids[idsindex] == 0
        global increment *= ids[idsindex]
        global  idsindex +=1
    end
    # Advance time
    global time += increment
end
println("part2:", time - increment)
