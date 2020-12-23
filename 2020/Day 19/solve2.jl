using Pipe: @pipe

rawrules = @pipe "./rules2.txt" |> readlines
rawdata = @pipe "./data.txt" |> readlines

letters = Dict(72 => "a", 58 => "b")

rules = Dict()
for r in rawrules
    s = split(r, ":")
    rules[parse(Int, s[1])] = split(strip(s[2]), " ")
end

first8 = true
first11 = true
create_matcher(number, rule) = begin
    matcher = ""
    for x in rule
        if x == "|"
            matcher *= x
        else 
            rule_number = parse(Int, x)
            if number == rule_number
                # matcher *= "<insert reccurse>"
                if number == 8
                    matcher =  matcher * "(?&eight)?"
                else
                    matcher =  matcher * "(?&eleven)?"
                end
            else
                if haskey(letters, rule_number)
                    matcher *= letters[rule_number]
                else
                    prefix = "(?" 
                    if rule_number == 8 && first8
                        prefix *= "<eight>"
                        global first8 = false
                    elseif rule_number == 11 && first11
                        prefix *= "<eleven>"
                        global first11 = false
                    else
                        prefix *= ":"
                    end
                    matcher *= prefix * create_matcher(rule_number, rules[rule_number]) * ")"
                end
            end
        end
    end
    return matcher
end

matcher = "^" * create_matcher(0, rules[0]) * "\$"

matcher = Regex(matcher)
nb = 0
for message in rawdata
    if occursin(matcher, message)
        global nb += 1
    end
end

println("part2: ", nb)
