using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "");

matrix = permutedims(hcat(rawValues...))

gamma = ""
epsilon = ""
for i = 1:length(rawValues[1])
    nb_ones = count(x -> x == "1", matrix[:, i])
    if nb_ones > length(rawValues) / 2
        global gamma *= "1"
        global epsilon *= "0"
    else
        global gamma *= "0"
        global epsilon *= "1"
    end
end

gamma = parse(Int, gamma, base = 2)
epsilon = parse(Int, epsilon, base = 2)

println("part1 ", gamma * epsilon)

oxygenValues = @pipe "./data.txt" |> readlines;
oxygen = ""

while length(oxygenValues) > 1
    nb_ones = count(x -> startswith(x, oxygen * "1"), oxygenValues)
    nb_zeros = count(x -> startswith(x, oxygen * "0"), oxygenValues)
    if nb_ones >= nb_zeros
        global oxygen *= "1"
    else
        global oxygen *= "0"
    end
    filter!(x -> startswith(x, oxygen), oxygenValues)
end

oxygen = parse(Int, oxygenValues[1], base = 2)

co2Values = @pipe "./data.txt" |> readlines;
co2 = ""

while length(co2Values) > 1
    nb_ones = count(x -> startswith(x, co2 * "1"), co2Values)
    nb_zeros = count(x -> startswith(x, co2 * "0"), co2Values)
    if nb_zeros <= nb_ones
        global co2 *= "0"
    else
        global co2 *= "1"
    end
    filter!(x -> startswith(x, co2), co2Values)
end

co2 = parse(Int, co2Values[1], base = 2)

println("part2 ", oxygen * co2)

