using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readlines |> split.(_, "");
opens = ["[", "(", "{", "<"];
closes = ["]", ")", "}", ">"];
for line in rawValues
    open = Dict()
    close = Dict()
    for symbol in line
        if contains(opens, symbol)
            if haskey(open, symbol)
                open[symbol] = open[symbol] + 1
            else
                open[symbol] = 1
            end
        else
            if contains(closes, symbol)
                if haskey(close, symbol)
                    close[symbol] = close[symbol] + 1
                else
                    close[symbol] = 1
                end
            end
        end

        println("symbol ", symbol)
    end
end
# println("rawValues ", rawValues)
