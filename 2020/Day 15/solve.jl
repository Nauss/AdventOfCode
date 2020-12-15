said = Dict(0 => (1, 1),
            14 => (2, 2),
            6 => (3, 3),
            20 => (4, 4),
            1 => (5, 5),
            4 => (6, 6))
# said = Dict(
#     0 => (1, 1),
#     3 => (2, 2),
#     6 => (3, 3),
# )

isspoken(i) = begin
    found = said[i]
    return found[2] - found[1]
end

say(number, index) = begin
    tmp = haskey(said, number) ? said[number][2] : index
    global said[number] = (tmp, index)
end

lastsaid = 4
for i = length(said)+1:2020
    global lastsaid = isspoken(lastsaid)
    say(lastsaid, i)
end
println("part1:", lastsaid)

said = Dict(0 => (1, 1),
            14 => (2, 2),
            6 => (3, 3),
            20 => (4, 4),
            1 => (5, 5),
            4 => (6, 6))
lastsaid = 4
for i = length(said)+1:30000000
    global lastsaid = isspoken(lastsaid)
    say(lastsaid, i)
end
println("part2:", lastsaid)
