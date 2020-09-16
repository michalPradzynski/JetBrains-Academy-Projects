inventory = {"water": 400, "milk": 540, "beans": 120, "money": 550, "cups": 9}

ESPRESSO = {"water": 250, "milk": 0, "beans": 16, "money": 4, "cups": 1}
LATTE = {"water": 350, "milk": 75, "beans": 20, "money": 7, "cups": 1}
CAPPUCCINO = {"water": 200, "milk": 100, "beans": 12, "money": 6, "cups": 1}


def log_machine_state(inventory):
    print(f"""
The coffee machine has:
{inventory["water"]} of water
{inventory["milk"]} of milk
{inventory["beans"]} of coffee beans
{inventory["cups"]} of disposable cups
${inventory["money"]} of money
""")


def coffee_buy(coffee_type):
    if coffee_type == "1":
        coffee_type = ESPRESSO
    elif coffee_type == "2":
        coffee_type = LATTE
    elif coffee_type == "3":
        coffee_type = CAPPUCCINO
    for key, value in inventory.items():
        if (value - coffee_type[key]) >= 0: # or (key == "cups" and coffee_type["cups"] > 0):
            if key == "money":
                value += coffee_type[key]
            else:
                value -= coffee_type[key]
            inventory[key] = value
        else:
            print(f"Sorry, not enough {key}")
            break
    else:
        print("I have enough resources, making you a coffee!")


def machine_fill():
    water_fill = int(input("Write how many ml of water do you want to add: "))
    milk_fill = int(input("Write how many ml of milk do you want to add: "))
    coffee_fill = int(input("Write how many grams of coffee beans do you want to add: "))
    cups_fill = int(input("Write how many disposable cups of coffee do you want to add: "))
    inventory["water"] += water_fill
    inventory["milk"] += milk_fill
    inventory["beans"] += coffee_fill
    inventory["cups"] += cups_fill


if __name__ == '__main__':
    while True:
        action = input("Write action (buy, fill, take, remaining, exit): ")

        if action == "buy":
            while True:
                which_coffee = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
                if which_coffee == "back":
                    break
                else:
                    coffee_buy(which_coffee)
                    break
        elif action == "fill":
            machine_fill()
        elif action == "take":
            money = inventory["money"]
            print(f"I gave you ${money}")
            inventory["money"] = 0
        elif action == "remaining":
            log_machine_state(inventory)
        elif action == "exit":
            break






