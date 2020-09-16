inventory = {"money": 550, "water": 400, "milk": 540, "beans": 120, "cups": 9}

espresso = {"water": 250, "milk": 0, "beans": 16, "cost": 4}
latte = {"water": 350, "milk": 75, "beans": 20, "cost": 7}
cappuccino = {"water": 200, "milk": 100, "beans": 12, "cost": 6}


def log_machine_state(inventory):
    print(f"""
The coffee machine has:
{inventory["water"]} of water
{inventory["milk"]} of milk
{inventory["beans"]} of coffee beans
{inventory["cups"]} of disposable cups
{inventory["money"]} of money
""")


def coffee_buy(coffee_type):
    if coffee_type == "1":
        coffee_type = espresso
    elif coffee_type == "2":
        coffee_type = latte
    elif coffee_type == "3":
        coffee_type = cappuccino
    inventory["water"] -= coffee_type["water"]
    inventory["milk"] -= coffee_type["milk"]
    inventory["beans"] -= coffee_type["beans"]
    inventory["cups"] -= 1
    inventory["money"] += coffee_type["cost"]


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
    log_machine_state(inventory)
    action = input("Write action (buy, fill, take): ")

    if action == "buy":
        what_coffee = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: ")
        coffee_buy(what_coffee)
        log_machine_state(inventory)
    elif action == "fill":
        machine_fill()
        log_machine_state(inventory)
    elif action == "take":
        money = inventory["money"]
        print(f"I gave you ${money}")
        inventory["money"] = 0
        log_machine_state(inventory)






