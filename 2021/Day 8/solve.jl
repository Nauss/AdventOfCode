using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "|");

signals = []
digits = []
for value in rawValues
    push!(signals, split(value[1]))
    push!(digits, split(value[2]))
end

part1 = Dict(0 => 0, 1 => 0, 2 => 0, 3 => 0, 4 => 0, 5 => 0, 6 => 0, 7 => 0, 8 => 0, 9 => 0)

for d in digits
    for w in d
        if length(w) == 2
            global part1[1] += 1
        elseif length(w) == 4
            global part1[4] += 1
        elseif length(w) == 3
            global part1[7] += 1
        elseif length(w) == 7
            global part1[8] += 1
        end
    end
end

println("part1 ", part1[1] + part1[4] + part1[7] + part1[8])

known_signals = Dict()
rewire_digit(rewire, digit) = replace(x -> rewire[x], digit)
signal_to_number = Dict("abcefg" => "0", "cf" => "1", "acdeg" => "2", "acdfg" => "3", "bcdf" => "4", "abdfg" => "5", "abdefg" => "6", "acf" => "7", "abcdefg" => "8", "abcdfg" => "9")
check(signals, digit, reference) = count(x -> contains(x, digit), signals) == reference

# For each line
part2 = 0
for line = 1:length(rawValues)
    rewire = Dict()
    line_signals = signals[line]
    for signal in line_signals
        if length(signal) == 2
            global known_signals['1'] = sort(collect(signal))
        elseif length(signal) == 4
            global known_signals['4'] = sort(collect(signal))
        elseif length(signal) == 3
            global known_signals['7'] = sort(collect(signal))
        elseif length(signal) == 7
            global known_signals['8'] = sort(collect(signal))
        end
    end

    # Rewire
    # One first
    one = known_signals['1']
    if check(line_signals, one[1], 8)
        rewire[one[1]] = 'c'
        rewire[one[2]] = 'f'
    else
        rewire[one[1]] = 'f'
        rewire[one[2]] = 'c'
    end
    # The seven
    seven = known_signals['7']
    filter!(x -> !haskey(rewire, x), seven)
    rewire[seven[1]] = 'a'
    # The four
    four = known_signals['4']
    filter!(x -> !haskey(rewire, x), four)
    if check(line_signals, four[1], 6)
        rewire[four[1]] = 'b'
        rewire[four[2]] = 'd'
    else
        rewire[four[1]] = 'd'
        rewire[four[2]] = 'b'
    end
    # The eight
    eight = known_signals['8']
    filter!(x -> !haskey(rewire, x), eight)
    if check(line_signals, eight[1], 4)
        rewire[eight[1]] = 'e'
        rewire[eight[2]] = 'g'
    else
        rewire[eight[1]] = 'g'
        rewire[eight[2]] = 'e'
    end

    output = ""
    for digit in digits[line]
        rewired = join(sort(rewire_digit(rewire, collect(digit))))
        output *= signal_to_number[rewired]
    end
    global part2 += parse(Int, output)
end

println("part2 ", part2)