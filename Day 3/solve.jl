using Pipe: @pipe

rules = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

part1 = @pipe "./data.txt" |> readlines |> split.(_, "");
height, width = length(part1), length(part1[1])
counts =   []
for rule in rules begin
        local col, count = 1 + rule[2],  0
        for row = 1 + rule[1]:rule[1]:length(part1) begin
                if part1[row][col] == "#"  count += 1 end
                col += rule[2]
                if col > width
                    col -= width
                end
            end
        end
    end
    push!(counts, count)
end
println("counts ", counts)
println("result ", reduce(*, counts))
