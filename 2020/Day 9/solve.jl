using Pipe: @pipe

data = @pipe "./data.txt" |>
read(_, String) |>
replace(_, "\n" => ";") |>
split.(_, ";");
data = parse.(Int, data)

check(preamble, value) = begin
    for i = 1:length(preamble)
        for j = 1:length(preamble)
            if i == j continue end
            if preamble[i] + preamble[j] == value return true end
        end
    end
    return false
end

index = 1
part1 = data[26]
for l = 27:length(data)
    if !check(data[index:index + 24], part1)
        break;
    end
    global index += 1
    global part1 = data[l]
end

println("part1: ", part1)

result = 0
for l = 1:length(data)
    for m = l + 1:length(data)
        s = sum(data[l:m])
        if s < part1
            continue
        elseif s > part1
            break
        else
            global result = min(data[l:m]...) + max(data[l:m]...)
            break
        end
    end
    if result != 0 break end
end
println("part2: ", result)
