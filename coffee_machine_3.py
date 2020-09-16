water = int(input("Write how many ml of water the coffee machine has:"))
milk = int(input("Write how many ml of milk the coffee machine has:"))
coffee_beans = int(input("Write how many grams of coffee beans the coffee machine has:"))
cups = int(input("Write how many cups of coffee you will need:"))

needed_water = 200
needed_milk = 50
needed_beans = 15

water_modulo = water // needed_water
milk_modulo = milk // needed_milk
beans_modulo = coffee_beans // needed_beans

max_no_of_cups = min(water_modulo, milk_modulo, beans_modulo)
if max_no_of_cups == cups:
    print("Yes, I can make that amount of coffee")
elif max_no_of_cups > cups:
    print(f"Yes, I can make that amount of coffee (and even {max_no_of_cups - cups} more than that)")
else:
    print(f"No, I can make only {max_no_of_cups} cups of coffee")


