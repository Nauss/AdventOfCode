using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, " -> ");
rules = Dict()
for (pair, element) in rawValues
    rules[pair] = element
end
polymer = "CKFFSCFSCBCKBPBCSPKP"

all_letters = Set()
for (_, letter) in rules
    push!(all_letters, letter)
end

function apply(polymer, rules)
    result = ""
    for i = 1:length(polymer)-1
        pair = polymer[i:i+1]
        result *= polymer[i] * rules[pair]
    end
    result *= last(polymer)
end

for i = 1:10
    global polymer = apply(polymer, rules)
end
polymer = split(polymer, "")
min_letter = Inf
max_letter = 0
for letter in all_letters
    occurences = count(x -> x == letter, polymer)
    if occurences < min_letter
        global min_letter = occurences
    end
    if occurences > max_letter
        global max_letter = occurences
    end
end
println("part1 ", max_letter - min_letter);

polymer = "CKFFSCFSCBCKBPBCSPKP"
result = Dict()
for i = 1:length(polymer)-1
    pair = polymer[i:i+1]
    if haskey(result, pair)
        result[pair] += 1
    else
        result[pair] = 1
    end
end
pair_rules = Dict()
for rule in rules
    pair_rules[rule[1]] = (rule[1][1] * rule[2], rule[2] * rule[1][2])
end
for i = 1:40
    new_result = Dict()
    for (pair, count) in result
        (pair1, pair2) = pair_rules[pair]
        if haskey(new_result, pair1)
            new_result[pair1] += count
        else
            new_result[pair1] = count
        end
        if haskey(new_result, pair2)
            new_result[pair2] += count
        else
            new_result[pair2] = count
        end
    end
    global result = new_result
end

counts = Dict()
for letter in all_letters
    for (pair, count) in result
        if contains(pair, letter)
            if !haskey(counts, letter)
                counts[letter] = 0
            end
            if pair == letter * letter
                counts[letter] += count
            else
                counts[letter] += (count / 2)
            end
        end
    end
    counts[letter] = floor(Int, counts[letter])
end
counts["C"] += 1
counts["P"] += 1

min_letter = Inf
max_letter = 0
for (letter, count) in counts
    if count < min_letter
        global min_letter = count
    end
    if count > max_letter
        global max_letter = count
    end
end
println("part2 ", max_letter - min_letter);