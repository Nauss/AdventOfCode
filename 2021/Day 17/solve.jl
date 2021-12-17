
mutable struct Point
    x::Int
    y::Int
end
xmin = 179
xmax = 201
ymin = -109
ymax = -63

function done(position)
    position.x >= xmin && position.y <= ymax
end

function ontarget(position)
    position.x >= xmin && position.x <= xmax && position.y <= ymax && position.y >= ymin
end

function shoot(velocity)
    max_height = 0
    position = Point(0, 0)
    while true
        position.x += velocity.x
        position.y += velocity.y
        if position.y > max_height
            max_height = position.y
        end
        if done(position)
            break
        end
        if velocity.x > 0
            velocity.x -= 1
        elseif velocity.x < 0
            velocity.x += 1
        else
            # velocity.x = 0
            if position.x < xmin
                break
            end
            if position.x > xmax
                break
            end
        end
        velocity.y -= 1
    end
    (position, max_height)
end

velocity_min_x = 1
while true
    vx = velocity_min_x
    position = 0
    while true
        position += vx
        vx -= 1
        if vx == 0
            break
        end
    end
    if position >= xmin
        break
    end
    global velocity_min_x += 1
end

velocity_max_y = 1000
while true
    vy = velocity_max_y
    position = 0
    while position > ymax
        position += vy
        vy -= 1
    end
    if position >= ymin
        break
    end
    global velocity_max_y -= 1
end

velocity = Point(velocity_min_x, velocity_max_y)
(position, max_height) = shoot(velocity)
println("part1 ", max_height)

part2 = 0

for x = velocity_min_x:velocity_min_x+1000
    for y = velocity_max_y:-1:velocity_max_y-1000
        (p,) = shoot(Point(x, y))
        if ontarget(p)
            global part2 += 1
        end
    end
end

println("part2 ", part2)
