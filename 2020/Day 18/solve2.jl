using Pipe: @pipe

rawdata = @pipe "./data.txt" |> readlines |> replace.(_, " " => "")

operators = ['+', '*']
digit = ['1', '2','3', '4','5', '6', '7', '8', '9', '0']

previous_index(expr, index) = begin
    result = index - 1
    if result <= 1 return 1 end
    open = []
    found = nothing
    while isnothing(found)
        c = expr[result]
        if c == ')'
            push!(open, result)
        end
        while length(open) != 0
            result = result - 1
            if expr[result] == ')'
                push!(open, result)
            elseif expr[result] == '('
                pop!(open)
            end
        end
        if result <= 1
            result = 1
            found = true
        elseif expr[result] in digit
            result = result - 1
        else
            if expr[result] != '('
                result = result + 1
            end
            found = true
        end
    end
    result
end

next_index(expr, index) = begin
    result = index + 1
    if result >= length(expr) return length(expr) end
    open = []
    found = nothing
    while isnothing(found)
        c = expr[result]
        if c == '('
            push!(open, result)
        end
        while length(open) != 0
            result = result + 1
            if expr[result] == '('
                push!(open, result)
            elseif expr[result] == ')'
                pop!(open)
            end
        end
        if result >= length(expr)
            found = true
        elseif expr[result] in digit
            result = result + 1
        else
            if expr[result] != ')'
                result = result - 1
            end
            found = true
        end
    end
    result
end

parens_next_plus(expr, start) = begin
    newexpr = deepcopy(expr)
    index = findfirst(x -> x == '+', newexpr)
    while !isnothing(index)
        previous = previous_index(newexpr, index)
        next = next_index(newexpr, index)
        result = "(" * newexpr[previous:index - 1] * ";" * newexpr[index + 1:next] * ")"
        if previous - 1 >= start
            result = newexpr[1:previous - 1] * result
        end
        if next + 1 <= length(newexpr)
            result = result * newexpr[next + 1:end]
        end
        newexpr = result
        index = findfirst(x -> x == '+', newexpr)
    end
    # No plus
    return replace(newexpr, ";" => "+")
end

sum = 0
for line in rawdata
    global sum += eval(Meta.parse(parens_next_plus(line, 1)))
end
println("part2:", sum)
