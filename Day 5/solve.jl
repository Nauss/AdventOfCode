using Pipe: @pipe

getvalue(line) = parse(Int, line[1:7], base=2) * 8 + parse(Int, line[8:10], base=2)

data = @pipe "./data.txt" |>
    readlines |>
    replace.(_, r"[FL]" => "0")  |>
    replace.(_, r"[BR]" => "1") |>
    getvalue.(_) |> sort;

println("part1: ", data[end])

current = data[1]
result = []
for i = 2:length(data)
    if current + 1 != data[i]
        push!(result, data[i])
    end
    global current = data[i]
end
println("result: ", result)
