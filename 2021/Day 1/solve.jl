using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines;
values = parse.(Int, rawValues);

diffs = similar(values);
for i = 2:length(values)
    diffs[i] = values[i] - values[i-1]
end
diffs[1] = diffs[2]
part1 = count(x -> x > 0, diffs)
println("part1 ", part1)

sums = similar(values);
for i = 3:length(values)
    sums[i] = values[i] + values[i-1] + values[i-2]
end
sums[1] = sums[3]
sums[2] = sums[3]
diffs2 = similar(sums);
for i = 2:length(sums)
    diffs2[i] = sums[i] - sums[i-1]
end
diffs2[1] = 0
part2 = count(x -> x > 0, diffs2)
println("part2 ", part2)
