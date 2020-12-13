using Pipe: @pipe

data = @pipe "./data.txt" |>
readlines |>
split.(_," ");

switch_index = 1
current_line = 1
acc = 0
current_line = 1
processed = []
while true
    global acc = 0
    global current_line = 1
    global processed = []
    while true
        if current_line in processed break end
        push!(processed, current_line)
        line = data[current_line]
        if line[1] == "acc"
            global acc += parse(Int, line[2])
            global current_line += 1
        else
            local op = line[1]
            if switch_index == current_line
                if op == "jmp" local op = "nop" else local op = "jmp" end
            end
            if op == "jmp"
                global current_line += parse(Int, line[2])
            else
                global current_line += 1
            end
        end
        if current_line > length(data)
            break
        end
    end
    if switch_index > length(data) || current_line == length(data) + 1 break end
    if switch_index == 1 println("part1: ", acc) end
    
    global switch_index += 1
end
println("part2: ", acc)
