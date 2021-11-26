using Pipe: @pipe

rules = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

part1 = @pipe "./data.txt" |> readlines;
println("data ", part1)
