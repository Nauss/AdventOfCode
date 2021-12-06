using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, ",")[1] |> parse.(Int, _);

fishes = copy(rawValues)
for epoch = 1:80
    newfish = []
    for f = 1:length(fishes)
        if fishes[f] == 0
            global fishes[f] = 6
            push!(newfish, 8)
        else
            global fishes[f] -= 1
        end
    end
    if length(newfish) != 0
        append!(fishes, newfish)
    end
end

println("part1 ", length(fishes))

part2 = count(x -> x == 0 || x != 0, rawValues)
fishes = Dict()
for i = 0:8
    fishes[i] = Int64(count(x -> x == i, rawValues))
end
for epoch = 1:256
    newfishes = fishes[0]
    # Day decrement
    global fishes[0] = fishes[1]
    global fishes[1] = fishes[2]
    global fishes[2] = fishes[3]
    global fishes[3] = fishes[4]
    global fishes[4] = fishes[5]
    global fishes[5] = fishes[6]
    global fishes[6] = fishes[7] + newfishes
    global fishes[7] = fishes[8]
    # Update the rest
    global fishes[8] = newfishes
    global part2 += newfishes
end

println("part2 ", part2)
