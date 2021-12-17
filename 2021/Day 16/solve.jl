using Pipe: @pipe

rawValues = @pipe "./data.txt" |> readline;
binary = ""
expression = "+("

function hex2string(hex)
    if hex == '0'
        return "0000"
    end
    if hex == '1'
        return "0001"
    end
    if hex == '2'
        return "0010"
    end
    if hex == '3'
        return "0011"
    end
    if hex == '4'
        return "0100"
    end
    if hex == '5'
        return "0101"
    end
    if hex == '6'
        return "0110"
    end
    if hex == '7'
        return "0111"
    end
    if hex == '8'
        return "1000"
    end
    if hex == '9'
        return "1001"
    end
    if hex == 'A'
        return "1010"
    end
    if hex == 'B'
        return "1011"
    end
    if hex == 'C'
        return "1100"
    end
    if hex == 'D'
        return "1101"
    end
    if hex == 'E'
        return "1110"
    end
    if hex == 'F'
        return "1111"
    end
end

for value in rawValues
    global binary *= hex2string(value)
end

part1 = 0
function get_version(message)
    version = message[1:3]
    message = chop(message, head = 3, tail = 0)
    value = parse(Int, version, base = 2)
    global part1 += value
    (value, message, 3)
end

function get_type(message)
    type = message[1:3]
    message = chop(message, head = 3, tail = 0)
    value = parse(Int, type, base = 2)
    (value, message, 3)
end

function last_group(message)
    islastgroup = string(first(message))
    message = chop(message, head = 1, tail = 0)
    value = parse(Int, islastgroup, base = 2) == 0
    (value, message, 2)
end

function get_literal(message)
    literal = message[1:4]
    message = chop(message, head = 4, tail = 0)
    (literal, message, 4)
end

function read_literal(message)
    nb_bits = 0
    (islastgroup, message, bits) = last_group(message)
    nb_bits += bits
    literal = ""
    while !islastgroup
        (l, message, bits) = get_literal(message)
        nb_bits += bits
        literal *= l
        (islastgroup, message, bits) = last_group(message)
        nb_bits += bits
    end
    # Get the last literal
    (l, message, bits) = get_literal(message)
    nb_bits += bits
    literal *= l
    value = parse(Int, literal, base = 2)
    (value, message, nb_bits)
end

function get_length(message)
    length_type = string(first(message))
    message = chop(message, head = 1, tail = 0)
    (length_type, message, 1)
end

function get_total_length(message)
    total_length = message[1:15]
    message = chop(message, head = 15, tail = 0)
    value = string(parse(Int, total_length, base = 2))
    (value, message, 15)
end

function get_sub_packets(message)
    sub_packets = message[1:11]
    message = chop(message, head = 11, tail = 0)
    value = parse(Int, sub_packets, base = 2)
    (value, message, 11)
end

function read_operator(message)
    nb_bits = 0
    (length, message, bits) = get_length(message)
    nb_bits += bits
    if length == "0"
        (total, message, bits) = get_total_length(message)
        nb_bits += bits
        to_read = parse(Int, total)
        while to_read > 0
            (packet, message, bits) = read_packet(message)
            nb_bits += bits
            to_read -= bits
        end
    else
        (sub, message, bits) = get_sub_packets(message)
        nb_bits += bits
        for i = 1:sub
            (packet, message, bits) = read_packet(message)
            nb_bits += bits
        end
    end
    ("", message, nb_bits)
end

function read_packet(message)
    nb_bits = 0
    (version, message, bits) = get_version(message)
    nb_bits += bits
    (type, message, bits) = get_type(message)
    nb_bits += bits
    if type == 4
        (literal, message, bits) = read_literal(message)
        nb_bits += bits
        global expression *= string(literal) * ","
    else
        if type == 0
            global expression *= "+("
        elseif type == 1
            global expression *= "*("
        elseif type == 2
            global expression *= "min("
        elseif type == 3
            global expression *= "max("
        elseif type == 5
            global expression *= ">("
        elseif type == 6
            global expression *= "<("
        elseif type == 7
            global expression *= "==("
        end
        (op, message, bits) = read_operator(message)
        nb_bits += bits
        global expression *= ")"
        if type == 5 || type == 6 || type == 7
            global expression *= " ? 1 : 0"
        end
        global expression *= ","
    end
    ("done", message, nb_bits)
end

while length(binary) > 8
    packet = read_packet(binary)
    global binary = packet[2]
end
expression *= ")"
println("part1 ", part1)
println("part2 ", eval(Meta.parse(expression)))
