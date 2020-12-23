using Pipe: @pipe

rawrules = @pipe "./rules.txt" |> readlines
rawdata = @pipe "./data.txt" |> readlines

letters = Dict(72 => "a", 58 => "b")

rules = Dict()
for r in rawrules
    s = split(r, ":")
    rules[parse(Int, s[1])] = split(strip(s[2]), " ")
end

create_matcher(rule) = begin
    matcher = ""
    for x in rule
        if x == "|"
            matcher *= x
        else 
            rule_number = parse(Int, x)
            if haskey(letters, rule_number)
                matcher *= letters[rule_number]
            else
                matcher *= "(" * create_matcher(rules[rule_number]) * ")"
            end
        end
    end
    return matcher
end

matcher = "^" * create_matcher(rules[0]) * "\$"
matcher = Regex(matcher)
nb = 0
for message in rawdata
    if occursin(matcher, message)
        global nb += 1
    end
end

print("part1: ", nb)