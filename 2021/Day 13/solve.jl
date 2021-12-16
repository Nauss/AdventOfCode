using Pipe: @pipe
using Images

rawValues = @pipe "./data.txt" |> readlines |> split.(_, ",");
original_dots = []
for value in rawValues
    push!(original_dots, (parse(Int, value[1]), parse(Int, value[2])))
end

function fold(dots, direction, position)
    new_dots = Set()
    if direction == "y"
        for dot in dots
            if dot[2] > position
                push!(new_dots, (dot[1], position - (dot[2] - position)))
            else
                push!(new_dots, (dot[1], dot[2]))
            end
        end
    else
        for dot in dots
            if dot[1] > position
                push!(new_dots, (position - (dot[1] - position), dot[2]))
            else
                push!(new_dots, (dot[1], dot[2]))
            end
        end
    end
    new_dots
end

current_fold = fold(original_dots, "x", 655)

println("part1 ", length(current_fold))

current_fold = fold(current_fold, "y", 447)
current_fold = fold(current_fold, "x", 327)
current_fold = fold(current_fold, "y", 223)
current_fold = fold(current_fold, "x", 163)
current_fold = fold(current_fold, "y", 111)
current_fold = fold(current_fold, "x", 81)
current_fold = fold(current_fold, "y", 55)
current_fold = fold(current_fold, "x", 40)
current_fold = fold(current_fold, "y", 27)
current_fold = fold(current_fold, "y", 13)
current_fold = fold(current_fold, "y", 6)

max_x = 0
max_y = 0
for dot in current_fold
    if dot[1] > max_x
        global max_x = dot[1]
    end
    if dot[2] > max_y
        global max_y = dot[2]
    end
end
result = fill(RGB(0, 0, 0), (max_y + 1, max_x + 1))
for dot in current_fold
    global result[dot[2]+1, dot[1]+1] = RGB(0.1, 0.1, 1)
end
display(result)
