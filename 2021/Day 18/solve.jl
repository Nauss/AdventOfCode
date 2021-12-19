using Pipe: @pipe
import Base.show

rawValues = @pipe "./data.txt" |> readlines |> Meta.parse.(_) |> eval.(_);

mutable struct SNumber
    left::Union{Int,SNumber}
    right::Union{Int,SNumber}
    depth::Int
    parent::Union{SNumber,Nothing}
end

EXPLODE_DEPTH = 4

function SNumber(number::Any, depth = 0, parent = nothing)
    if length(number) == 1
        return SNumber(number[0], depth + 1, parent)
    end
    left = number[1]
    right = number[2]
    if isa(left, Int)
        if isa(right, Int)
            return SNumber(left, right, depth, parent)
        else
            newnumber = SNumber(left, 0, depth, parent)
            newnumber.right = SNumber(right, depth + 1, newnumber)
            return newnumber
        end
    else
        if isa(right, Int)
            newnumber = SNumber(0, right, depth, parent)
            newnumber.left = SNumber(left, depth + 1, newnumber)
            return newnumber
        else
            newnumber = SNumber(0, 0, depth, parent)
            newnumber.left = SNumber(left, depth + 1, newnumber)
            newnumber.right = SNumber(right, depth + 1, newnumber)
            return newnumber
        end
    end
end

function tostring(n::SNumber)
    left = ""
    if isa(n.left, SNumber)
        left = tostring(n.left)
    elseif isa(n.left, Int)
        left = string(n.left)
    end
    right = ""
    if isa(n.right, SNumber)
        right = tostring(n.right)
    elseif isa(n.right, Int)
        right = string(n.right)
    end
    result = "[" * left * "," * right * "]"
    result
end

show(io::IO, n::SNumber) = show(io::IO, tostring(n))

function isparent(n::SNumber, parent::SNumber)
    current = n.parent
    while current !== nothing
        if current == parent
            return true
        end
        current = current.parent
    end
    return false
end

function first_left(n::SNumber)
    if isa(n.right, Int)
        return n
    else
        return first_left(n.right)
    end
end

function next_left(n::SNumber)
    current = n
    parent = n.parent
    while parent !== nothing
        if parent.left != current
            if isa(parent.left, Int)
                return (parent, "left")
            else
                return (first_left(parent.left), "right")
            end
        end
        current = parent
        parent = parent.parent
    end
end

function first_right(n::SNumber)
    if isa(n.left, Int)
        return n
    else
        return first_right(n.left)
    end
end

function next_right(n::SNumber)
    current = n
    parent = n.parent
    while parent !== nothing
        if parent.right != current
            if isa(parent.right, Int)
                return (parent, "right")
            else
                return (first_right(parent.right), "left")
            end
        end
        current = parent
        parent = parent.parent
    end
end

function explode(root::SNumber, n::SNumber)
    isleft = n == n.parent.left
    reseted = false
    # Explode left
    next = next_left(n)
    if next !== nothing
        if next[2] == "left"
            next[1].left += n.left
        else
            next[1].right += n.left
        end
    else
        n.parent.left = 0
        reseted = true
    end
    # Explode right
    next = next_right(n)
    if next !== nothing
        if next[2] == "left"
            next[1].left += n.right
        else
            next[1].right += n.right
        end
    else
        n.parent.right = 0
        reseted = true
    end

    if !reseted
        if isleft
            n.parent.left = 0
        else
            n.parent.right = 0
        end
    end
end

function split(n::SNumber)
    if isa(n.left, Int)
        if n.left >= 10
            n.left = SNumber(floor(Int, n.left / 2), ceil(Int, n.left / 2), n.depth + 1, n)
            return true
        end
    else
        if split(n.left)
            return true
        end
    end
    if isa(n.right, Int)
        if n.right >= 10
            n.right = SNumber(floor(Int, n.right / 2), ceil(Int, n.right / 2), n.depth + 1, n)
            return true
        end
    else
        if split(n.right)
            return true
        end
    end
    false
end

function need_explode(n::SNumber)
    if n.depth >= EXPLODE_DEPTH
        result = n
        while isa(result.left, SNumber) || isa(result.right, SNumber)
            if isa(result.left, SNumber)
                result = result.left
            elseif isa(result.right, SNumber)
                result = result.right
            end
        end
        return result
    end
    if isa(n.left, SNumber)
        result = need_explode(n.left)
        if result !== nothing
            return result
        end
    end
    if isa(n.right, SNumber)
        result = need_explode(n.right)
        if result !== nothing
            return result
        end
    end
    return nothing
end

function reduce(n::SNumber)
    toexplode = need_explode(n)
    while toexplode !== nothing
        explode(n, toexplode)
        toexplode = need_explode(n)
    end

    splitted = split(n)
    if splitted
        reduce(n)
    end
end

function udpate_depth(n::SNumber)
    n.depth += 1
    if isa(n.left, SNumber)
        udpate_depth(n.left)
    end
    if isa(n.right, SNumber)
        udpate_depth(n.right)
    end
end

function add(left::SNumber, right::SNumber)
    result = SNumber(left, right, 0, nothing)
    left.parent = result
    right.parent = result
    # Update depth
    udpate_depth(left)
    udpate_depth(right)
    result
end

function magnitude(n::SNumber)
    result = 0
    if isa(n.left, Int)
        result += 3 * n.left
    else
        result += 3 * magnitude(n.left)
    end
    if isa(n.right, Int)
        result += 2 * n.right
    else
        result += 2 * magnitude(n.right)
    end
    result
end

current = SNumber(rawValues[1])
reduce(current)
for i = 2:length(rawValues)
    right = SNumber(rawValues[i])
    reduce(right)
    global current = add(current, right)
    reduce(current)
end
println("part1 ", magnitude(current))

part2 = 0
for a in rawValues
    for b in rawValues
        if a != b
            result = add(SNumber(a), SNumber(b))
            reduce(result)
            result = magnitude(result)
            if result > part2
                global part2 = result
            end
            result = add(SNumber(b), SNumber(a))
            reduce(result)
            result = magnitude(result)
            if result > part2
                global part2 = result
            end
        end
    end
end
println("part1 ", part2)
