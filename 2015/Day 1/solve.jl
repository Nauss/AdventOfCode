using Pipe: @pipe

part1 = @pipe "./data.txt" |> read(_, String) |> split.(_, "");

floor = 0
index = 0
for i = 1:length(part1)
    step = part1[i]
    if step == "("
        global floor = floor + 1
    end
    if step == ")"
        global floor = floor - 1
    end
    if floor == -1 && index == 0
        global index = i
    end
end
println("part1 ", floor)
println("part2 ", index)
