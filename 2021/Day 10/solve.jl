using Pipe: @pipe
using Statistics

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "");
opens = "[({<"

opposite = Dict("(" => ")", "{" => "}", "[" => "]", "<" => ">");
error_points = Dict(")" => 3, "]" => 57, "}" => 1197, ">" => 25137)
closing_points = Dict(")" => 1, "]" => 2, "}" => 3, ">" => 4)
part1 = 0
part2 = []
incompletes = []
for line in rawValues
    open = []
    is_incomplete = true
    for symbol in line
        if contains(opens, symbol)
            push!(open, symbol)
        else
            if opposite[last(open)] == symbol
                pop!(open)
            else
                global part1 += error_points[symbol]
                is_incomplete = false
                break
            end
        end
    end
    if is_incomplete
        sum = 0
        while length(open) > 0
            sum = 5 * sum + closing_points[opposite[last(open)]]
            pop!(open)
        end
        push!(part2, sum)
    end

end
println("part1 ", part1)
println("part2 ", Int(median(part2)))
