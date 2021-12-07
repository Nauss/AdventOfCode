using Pipe: @pipe
using Statistics

rawValues = @pipe "./data.txt" |> readlines |> split.(_, ",")[1] |> parse.(Int, _);

function compute_fuel1(position)
    sum(abs.(rawValues .- position))
end

m = Int(median(rawValues));

part1 = compute_fuel1(m)

println("part1 ", part1)

function compute_fuel2(position)
    result = 0
    distances = abs.(rawValues .- position)
    for distance in distances
        result = result + sum(1:distance)
    end
    result
end

m = Int(trunc(mean(rawValues)));

part1 = compute_fuel1(m)

println("part2 ", part2)