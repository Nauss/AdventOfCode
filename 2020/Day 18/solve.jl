using Pipe: @pipe

rawdata = @pipe "./data.txt" |> readlines |> replace.(_, " " => "")

operators = ['+', '*']

evaluate(expr) = begin
    newexpr = deepcopy(expr)
    open = []   # The indices of current open parenthesis
    firstop = -1     # Index of the first useable operator
    nextop = -1     # Index of the next useable operator
    for i = 1:length(expr)
        c = expr[i]
        if c in operators
            if firstop == -1
                firstop = i
            elseif length(open) == 0
                nextop = i
            end
        end
        if c == '(' push!(open, i) end
        if c == ')' 
            openstart = pop!(open)
            subexpr = evaluate(newexpr[openstart + 1:i - 1])
            return evaluate(newexpr[1:openstart - 1] * "$subexpr" * newexpr[i + 1:end])
        else
            if nextop != -1 && length(open) == 0
                value = eval(Meta.parse(newexpr[1:nextop - 1]))
                return evaluate("$value" * newexpr[nextop:end])
            end
        end
    end
    return eval(Meta.parse(newexpr))
end

sum = 0
for line in rawdata
    global sum += evaluate(line)
end
println("part1:", sum)
