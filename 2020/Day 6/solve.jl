using Pipe: @pipe

data = @pipe "./data.txt" |>
    read(_, String) |>
    replace(_, r"\n\n" => ";") |>
    replace(_, r"\n" => "-") |>
    split(_,";");

sum = 0
for d in data
    local result = Set()
    push!(result, replace.(d, "-" => "")...)
    global sum += length(result)
end
    
println("part1: ", sum)

sum = 0
for d in data
    local result = Dict()
    local size = length(split(d, "-"))
    for l in replace.(d, "-" => "")
        push!(result, l => haskey(result, l) ? result[l] + 1 : 1)
    end
    for r in result
        if size == r[2]
            global sum += 1
        end
    end
end
println("part2: ", sum)
