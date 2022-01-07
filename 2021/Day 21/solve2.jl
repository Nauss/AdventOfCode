function move(position, dice)
    new_position = (position + dice) % 10
    if new_position == 0
        new_position = 10
    end
    new_position
end

all_rolls = Dict()
for i = 1:3
    for j = 1:3
        for k = 1:3
            if !haskey(all_rolls, i + j + k)
                all_rolls[i+j+k] = 0
            end
            all_rolls[i+j+k] += 1
        end
    end
end

function play(position1, score1, position2, score2)
    # player 2 wins ?
    if score2 <= 0
        return (0, 1)
    end

    wins1, wins2 = 0, 0
    for (roll, nb_rolls) in all_rolls
        position1_ = move(position1, roll)
        (w2, w1) = play(position2, score2, position1_, score1 - position1_)
        wins1 += nb_rolls * w1
        wins2 += nb_rolls * w2
    end

    return (wins1, wins2)
end

wins = play(10, 21, 9, 21)
println("part2 ", wins)
