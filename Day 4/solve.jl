using Pipe: @pipe

validbyr = v -> begin
    length(v) == 4 && (1920 <= parse(Int, v) <= 2002)
end
validiyr = v -> begin
    length(v) == 4 && (2010 <= parse(Int, v) <= 2020)
end
valideyr = v -> begin
    length(v) == 4 && (2020 <= parse(Int, v) <= 2030)
end
validhgt = v -> begin
    m = match(r"(\d{1,3})(cm|in)", v)
    return !isnothing(m) && length(m.captures) >= 2 && (
            (m.captures[2] == "cm" && (150 <= parse(Int, m.captures[1]) <= 193)) ||
            (m.captures[2] == "in" && (59 <= parse(Int, m.captures[1]) <= 76)))
end
validhcl = v -> occursin(r"^#(\d|[a-f]){6}$", v)
eyecolor = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
validecl = v -> v in eyecolor
validpid = v -> occursin(r"^\d{9}$", v)

requested = ["byr","ecl","eyr","hcl","hgt","iyr","pid"]
valid = Dict("byr" => validbyr, "ecl" => validecl, "eyr" => valideyr, "hcl" => validhcl, "hgt" => validhgt, "iyr" => validiyr, "pid" => validpid)
isrequested(f) = f[1] in requested
extract(m) = (m.captures[1], m.captures[2])
isvalid(m) = begin
    key = findfirst(x -> x == m[1], requested)
    checker = valid[requested[key]]
    checker((m[2]))
end

data = @pipe "./data.txt" |>
    read(_, String) |>
    replace(_, r"\n\n" => ";") |>
    replace(_, r"\n" => " ") |>
    split.(_, ";");

count = 0
for p in data
    local result = @pipe eachmatch(r"(...):(.*?)([\s\n]|$)", p) |> collect |> extract.(_) |> filter(isrequested, _);
    if (length(requested) == length(result))
        global count +=   1 
    end
end

println("part1: ", count)

count = 0
for p in data
    local result = @pipe eachmatch(r"(...):(.*?)([\s\n]|$)", p) |> collect |> extract.(_) |> filter(isrequested, _) |> isvalid.(_);
    if (sum(result) == length(requested))
        global count +=   1 
    end
end
println("part2: ", count)
