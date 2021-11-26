using Pipe: @pipe

rawdata = @pipe "./data.txt" |> readlines

struct Ingredient
    name::String
    allergen::String
end
struct Food
    ingredients::Vector{Ingredient}
    allergens::Vector{String}
end
show(str::String) = begin
    print(str)
end
show(ingredient::Ingredient) = begin
    println("  name: $(ingredient.name)")
    println("  allergen: $(ingredient.allergen == "" ? "NA" : ingredient.allergen)")
end
show(food::Food) = begin
    println("")
    println("--------------------")
    println("ingredients:")
    show.(food.ingredients)
    println("")
    println("allergens:")
    show.(food.allergens)
    println("")
    println("--------------------")
end

all_ingredients = Set()
all_allergens= Set()
foods = []
line_regex = r"^(.*) \(contains (.*)\)$"
for line in rawdata
    result = match(line_regex, line)
    ingredients = @pipe result.captures[1] |> split |> Ingredient.(_, "")
    push!(all_ingredients, [i.name for i in ingredients]...)
    allergens = split(result.captures[2], ",")
    push!(all_allergens, allergens...)
    push!(foods, Food(ingredients, allergens))
end

# Start with all the ingredients having all the allergens
# discrad step by step
# OR
# Start empty
# add only when found and sure

# Loop each time an ingredient allergen is found

println("part1: ", foods)
show.(foods)
println("all_ingredients: ", all_ingredients)
println("all_allergens: ", all_allergens)
