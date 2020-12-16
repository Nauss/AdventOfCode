using Pipe: @pipe

rules = Dict(
"departure location" => [(32, 209), (234, 963)],
"departure station" => [(47, 64), (83, 967)],
"departure platform" => [(37, 609), (628, 970)],
"departure track" => [(29, 546), (567, 971)],
"departure date" => [(50, 795), (816, 960)],
"departure time" => [(49, 736), (750, 962)],
"arrival location" => [(48, 399), (420, 967)],
"arrival station" => [(49, 353), (360, 967)],
"arrival platform" => [(37, 275), (298, 969)],
"arrival track" => [(40, 119), (127, 954)],
"class" => [(35, 750), (760, 968)],
"duration" => [(43, 162), (186, 963)],
"price" => [(30, 889), (914, 949)],
"route" => [(39, 266), (274, 950)],
"row" => [(45, 366), (389, 954)],
"seat" => [(42, 765), (772, 955)],
"train" => [(30, 494), (518, 957)],
"type" => [(48, 822), (835, 973)],
"wagon" => [(32, 330), (342, 951)],
"zone" => [(36, 455), (462, 973)],
)

rawdata = @pipe "./data.txt" |> readlines |> split.(_, ",");
data = []
for i = 1:length(rawdata)
    push!(data, parse.(Int, rawdata[i]))
end

checkrule(rule, value) = begin
    result = false
    for range in rule[2]
        if range[1] <=  value <= range[2]
            result = true
        end
    end
    return result
end

check(ticket) = begin
    for value in ticket
        rulesok = false
        for rule in rules
            if checkrule(rule, value)
                rulesok = true
            end
        end
        if !rulesok return value end
    end
    return nothing
end

part1 = 0
data2 = []
for i = 2:length(data)
    c = check(data[i])
    if !isnothing(c)
        global part1 += c
    else
        push!(data2, data[i])
    end
end
println("part1:", part1)

nbfields = 20
fields = Dict() # (name, index)

get_okindices() = begin
    okindices = [i for i = 1:nbfields]
    for field in fields
        filter!(x -> x != field[2], okindices)
    end
    return okindices
end
checkfields() = begin
    for rule in rules
        if haskey(fields, rule[1]) continue end
        okindices = get_okindices()
        fail_indices = []
        for ticket in data2
            for index = 1:length(ticket)
                value = ticket[index]
                if !checkrule(rule, value)
                    push!(fail_indices, index)
                end
            end
            filter!(x -> x ∉ fail_indices, okindices)
        end
        if length(okindices) == 1 
            global fields[rule[1]] = okindices[1]
            return
        end
    end
end

while length(fields) != nbfields
    checkfields()
end


part2 = 1
for field in fields
    if occursin("departure", field[1])
        global part2 *= data[1][field[2]]
    end
end
println("part2:", part2)
