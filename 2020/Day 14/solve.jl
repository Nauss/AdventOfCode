using Pipe: @pipe

data = @pipe "./data.txt" |> readlines;

maskre = r"mask = ([X01]{36})"
memre = r"mem\[(\d*)\] = (\d*)"

struct Operation
    mask::String
    mem::Vector{Pair}
end

operations = []
operation = nothing
for line in data
    m = match(maskre, line)
    if !isnothing(m)
        # New operation
        # Save the previous one if any
        if !isnothing(operation) push!(operations, operation) end
        global operation = Operation(m.captures[1], [])
        continue
    end
    m = match(memre, line)
    push!(operation.mem, Pair(parse(Int, m.captures[1]), parse(Int, m.captures[2])))
end
# push the last one
push!(operations, operation)

applymask(mask, value) = begin
    result = collect(bitstring(value))
    paddedmask = "X"^(length(result) - length(mask)) * mask
    for i=1:length(result)
        if paddedmask[i] != 'X'
            result[i] = paddedmask[i]
        end
    end
    parse(BigInt, String(result), base = 2)
end

result = Dict()
for op in operations
    for m in op.mem
        result[m[1]] = applymask(op.mask, m[2])
    end
end
part1 = 0
for value in result
    global part1 += value[2]
end
println("part1:", part1)

applymaskv2(mask, address) = begin
    result = collect(bitstring(address))
    paddedmask = "0"^(length(result) - length(mask)) * mask
    for i=1:length(result)
        if paddedmask[i] != '0'
            result[i] = paddedmask[i]
        end
    end
    return String(result)
end

create_masks(mask) = begin
    nbx = count(x -> x == 'X', mask)
    result = []
    for i=0:2^nbx-1
        bits = bitstring(i)
        realmask = deepcopy(mask)
        index = lastindex(bits)
        while occursin(r"X", realmask)
            realmask = replace(realmask, r"X" => "$(bits[index])", count=1)
            index -= 1
        end
        push!(result, realmask)
    end
    return result
end

result = Dict()
for op in operations
    for m in op.mem
        adresses = create_masks(applymaskv2(op.mask, m[1]))
        for address in adresses
            result[parse(BigInt, address, base = 2)] = m[2]
        end
    end
end
part2 = 0
for value in result
    global part2 += value[2]
end
println("part2:", part2)