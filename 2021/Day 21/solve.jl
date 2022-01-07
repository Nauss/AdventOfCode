using Pipe: @pipe

mutable struct Player
    position::Int
    score::Int
end
function move(player::Player, value::Int)
    new_position = (player.position + value) % 10
    if new_position == 0
        player.position = 10
    else
        player.position = new_position
    end
    player.score += player.position
end

mutable struct Dice100
    current::Int
end

mutable struct Dice3
    current::Int
end

function roll(dice::Dice100)
    result = dice.current
    dice.current += 1
    if dice.current > 100
        dice.current = 1
    end
    result
end

player1 = Player(10, 0)
player2 = Player(9, 0)
dice = Dice100(1)

function play(player, dice::Dice100)
    move(player, roll(dice) + roll(dice) + roll(dice))
end

nb_rolls = 0
while player2.score < 1000
    play(player1, dice)
    global nb_rolls += 1
    if player1.score >= 1000
        break
    end
    play(player2, dice)
    global nb_rolls += 1
end
println("player1 ", player1)
println("player2 ", player2)
println("nb_rolls ", nb_rolls)
part1 = min(player1.score, player2.score) * nb_rolls * 3
println("part1 ", part1)
