using Pipe: @pipe
using CSV, DataFrames

numbers = [15, 62, 2, 39, 49, 25, 65, 28, 84, 59, 75, 24, 20, 76, 60, 55, 17, 7, 93, 69, 32, 23, 44, 81, 8, 67, 41, 56, 43, 89, 95, 97, 61, 77, 64, 37, 29, 10, 79, 26, 51, 48, 5, 86, 71, 58, 78, 90, 57, 82, 45, 70, 11, 14, 13, 50, 68, 94, 99, 22, 47, 12, 1, 74, 18, 46, 4, 6, 88, 54, 83, 96, 63, 66, 35, 27, 36, 72, 42, 98, 0, 52, 40, 91, 33, 21, 34, 85, 3, 38, 31, 92, 9, 87, 19, 73, 30, 16, 53, 80]
boards = CSV.read("./data.txt", DataFrame, header = false, delim = " ", ignorerepeated = true)

# Replace all number occurrences wiht -1
function draw!(boards, number)
    for row = 1:nrow(boards)
        for col = 1:5
            if boards[row, col] == number
                boards[row, col] = -1
            end
        end
    end
end

# Compute the final result of the board
function getresult(boards, number, reset = false)
    sum = 0
    is_5 = number % 5 == 0
    start_row = is_5 ? number - 4 : Int(trunc(number / 5) * 5 + 1)
    end_row = is_5 ? number : Int(trunc(number / 5) * 5 + 5)
    for row = start_row:end_row
        for col = 1:5
            if boards[row, col] != -1
                sum += boards[row, col]
            end
            if reset
                boards[row, col] = 1000
            end
        end
    end
    sum
end

# Check whether a board is winning
function check(boards, reset = false)
    for row = 1:nrow(boards)
        # Check rows
        if (sum(boards[row, 1:5]) == -5)
            # Win
            return getresult(boards, row, reset)
        end
        # Then cols
        if row % 5 == 0
            for col = 1:5
                if (sum(boards[row-4:row, col]) == -5)
                    # Win
                    return getresult(boards, row, reset)
                end
            end
        end
    end
    0
end

part1 = 0
for n in numbers
    draw!(boards, n)
    local result = check(boards)
    if result != 0
        global part1 = n * result
        break
    end
end

println("part1 ", part1)

boards = CSV.read("./data.txt", DataFrame, header = false, delim = " ", ignorerepeated = true)

part2 = 0
nb_winners = 0
done = false
for n in numbers
    draw!(boards, n)
    global part2 = check(boards, true)
    while part2 != 0
        global nb_winners += 1
        if nb_winners == 100 || n == last(numbers)
            global part2 = n * part2
            global done = true
            break
        end
        global part2 = check(boards, true)
    end
    if done
        break
    end
end
println("part2 ", part2)
