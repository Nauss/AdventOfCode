using Pipe: @pipe

data = @pipe "./data.txt" |>
    readlines |>
    replace.(_, r"\." => s"") |>
    replace.(_, r"contain" => s",") |>
    split.(_,",");

rules = Dict()
for line in data
    name = match(r"(.*) bags", line[1])[1]
    bags = Dict()
    for b=2:length(line)
        m = match(r"(\d) (.*) bags?", line[b])
        if !isnothing(m) bags[m[2]] = m[1] end
    end
    rules[name]=bags
end

check(rule) = begin
    if rule[1] == "shiny gold" return true end
    for (key, value) in rule[2]
        if check(key => rules[key]) 
            return true
         end
    end
    return false
end

result = Set()
for rule in rules
if check(rule)
    push!(result, rule[1])
end
end
println("part1: ", length(result) - 1)  # -1 for the definition of the shiny gold bag

count(rule) = begin
    sum = rule[1] == "shiny gold" ?  0 : 1
    for (key, value) in rule[2]
        sum += parse(Int, value) * count(key => rules[key])
    end
    return sum
end
println("part1: ", count("shiny gold" => rules["shiny gold"]))
