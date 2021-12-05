using Pipe: @pipe

struct Line
    x1::Int
    y1::Int
    x2::Int
    y2::Int
end

Line(captures) = Line(parse(Int, captures[1]), parse(Int, captures[2]), parse(Int, captures[3]), parse(Int, captures[4]))
line_regex = r"(\d+),(\d+) -> (\d+),(\d+)"

isdiagonal(line) = line.x1 != line.x2 && line.y1 != line.y2
is45(line) = abs(line.x1 - line.x2) == abs(line.y1 - line.y2)

rawValues = @pipe "./data.txt" |> readlines |> match.(line_regex, _) |> map(x -> Line(x.captures), _);

board = Dict()

for line in rawValues
    if !isdiagonal(line)
        xmin = min(line.x1, line.x2)
        xmax = max(line.x1, line.x2)
        ymin = min(line.y1, line.y2)
        ymax = max(line.y1, line.y2)
        for x = xmin:xmax
            for y = ymin:ymax
                if (haskey(board, (x, y)))
                    board[(x, y)] += 1
                else
                    board[(x, y)] = 1
                end
            end
        end
    end
end

part1 = count(x -> x.second >= 2, board)
println("part1 ", part1)

for line in rawValues
    if is45(line)
        xstep = line.x1 < line.x2 ? 1 : -1
        ystep = line.y1 < line.y2 ? 1 : -1
        x = line.x1
        y = line.y1
        for i = 1:abs(line.x1 - line.x2)+1
            if (haskey(board, (x, y)))
                board[(x, y)] += 1
            else
                board[(x, y)] = 1
            end
            x += xstep
            y += ystep
        end
    end
end

part2 = count(x -> x.second >= 2, board)
println("part2 ", part2)