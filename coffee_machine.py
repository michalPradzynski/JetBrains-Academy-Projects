class CoffeeMachine:
    inventory = {"water": 400, "milk": 540, "beans": 120, "money": 550, "cups": 9}

    ESPRESSO = {"water": 250, "milk": 0, "beans": 16, "money": 4, "cups": 1}
    LATTE = {"water": 350, "milk": 75, "beans": 20, "money": 7, "cups": 1}
    CAPPUCCINO = {"water": 200, "milk": 100, "beans": 12, "money": 6, "cups": 1}

    log_machine_state = f"""
    The coffee machine has:
    {inventory["water"]} of water
    {inventory["milk"]} of milk
    {inventory["beans"]} of coffee beans
    {inventory["cups"]} of disposable cups
    ${inventory["money"]} of money
    """

    def coffee_buy(self, coffee_type):
        if coffee_type == "1":
            coffee_type = self.ESPRESSO
        elif coffee_type == "2":
            coffee_type = self.LATTE
        elif coffee_type == "3":
            coffee_type = self.CAPPUCCINO
        for key, value in self.inventory.items():
            if (value - coffee_type[key]) >= 0: # or (key == "cups" and coffee_type["cups"] > 0):
                if key == "money":
                    value += coffee_type[key]
                else:
                    value -= coffee_type[key]
                self.inventory[key] = value
            else:
                print(f"Sorry, not enough {key}")
                break
        else:
            print("I have enough resources, making you a coffee!")

    def machine_fill(self):
        water_fill = int(input("Write how many ml of water do you want to add: "))
        milk_fill = int(input("Write how many ml of milk do you want to add: "))
        coffee_fill = int(input("Write how many grams of coffee beans do you want to add: "))
        cups_fill = int(input("Write how many disposable cups of coffee do you want to add: "))
        self.inventory["water"] += water_fill
        self.inventory["milk"] += milk_fill
        self.inventory["beans"] += coffee_fill
        self.inventory["cups"] += cups_fill

    def machine_logic(self, action):
        while True:
            if action == "buy":
                while True:
                    which_coffee = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
                    if which_coffee == "back":
                        break
                    else:
                        self.coffee_buy(which_coffee)
                        break
            elif action == "fill":
                self.machine_fill()
            elif action == "take":
                money = self.inventory["money"]
                print(f"I gave you ${money}")
                self.inventory["money"] = 0
            elif action == "remaining":
                print(self.log_machine_state)
            elif action == "exit":
                break


coffee = CoffeeMachine()
coffee.machine_logic(input("Write action (buy, fill, take, remaining, exit): "))
