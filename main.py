import time

class CoffeeMachine:
    def __init__(self):
        """Initialize machine resources and drink recipes."""
        self.resources = {"Milk": 8000, "Water": 5000, "Coffee": 600, "Sugar Packets": 100}
        self.choices = {
            "Cappuccino": {
                "Large":  {"Milk": 300, "Water": 350, "Coffee": 75, "Price": 5.00},
                "Medium": {"Milk": 200, "Water": 250, "Coffee": 50, "Price": 4.00},
                "Small":  {"Milk": 120, "Water": 150, "Coffee": 30, "Price": 3.00}
            },
            "Espresso": {
                "Large":  {"Water": 60,  "Coffee": 35, "Price": 4.50},
                "Medium": {"Water": 50,  "Coffee": 30, "Price": 3.50},
                "Small":  {"Water": 40,  "Coffee": 25, "Price": 2.50}
            },
            "Macchiato": {
                "Large":  {"Milk": 120, "Water": 70, "Coffee": 30, "Price": 5.50},
                "Medium": {"Milk": 100, "Water": 60, "Coffee": 25, "Price": 4.50},
                "Small":  {"Milk": 80,  "Water": 50, "Coffee": 20, "Price": 3.50}
            },
            "Black": {
                "Large":  {"Water": 300, "Coffee": 30, "Price": 4.00},
                "Medium": {"Water": 220, "Coffee": 25, "Price": 3.00},
                "Small":  {"Water": 150, "Coffee": 20, "Price": 2.00}
            },
            "Americano": {
                "Large":  {"Water": 350, "Coffee": 30, "Price": 4.50},
                "Medium": {"Water": 250, "Coffee": 25, "Price": 3.50},
                "Small":  {"Water": 180, "Coffee": 20, "Price": 2.50}
            },
            "Mocha": {
                "Large":  {"Milk": 180, "Water": 150, "Coffee": 35, "Price": 6.00},
                "Medium": {"Milk": 140, "Water": 120, "Coffee": 30, "Price": 5.00},
                "Small":  {"Milk": 100, "Water": 100, "Coffee": 25, "Price": 4.00}
            }
        }

    def report(self):
        """Display the current amount of all machine resources."""
        print("\nMachine resources left:")
        for item, amount in self.resources.items():
            unit = "g" if item == "Coffee" else "ml"
            print(f" - {item}: {amount}{unit}")

    def check_resources(self, drink, size):
        """
        Verify if enough resources exist to prepare the selected drink and size.
        Includes a separate check for sugar packets.
        """
        required = self.choices[drink][size]
        for item, amount_needed in required.items():
            if item == "Price":
                continue
            if self.resources.get(item, 0) < amount_needed:
                unit = "g" if item == "Coffee" else "ml"
                print(f"Not enough {item}! Needed: {amount_needed}{unit}, Available: {self.resources.get(item,0)}{unit}")
                return False
        if self.resources.get("Sugar Packets", 0) <= 0:
            print("Not enough sugar packets! Please refill the machine.")
            return False    
        print("All resources available!")
        return True

    def coins(self):
        """
        Ask the user for coin inputs and calculate the total inserted amount.
        Handles invalid and negative inputs safely.
        """
        coin_values = {
            "pennies": 0.01,
            "nickels": 0.05,
            "dimes": 0.1,
            "quarters": 0.25,
            "dollars": 1
        }
        total = 0
        for coin, value in coin_values.items():
            while True:
                user_input = input(f"How many {coin}? ").strip()
                if user_input == "":
                    amount = 0
                else:
                    try:
                        amount = int(user_input)
                        if amount < 0:
                            print("Please enter a non-negative number")
                            continue
                    except ValueError:
                        print("Invalid number. Try again.")
                        continue
                total += amount * value
                break
        print(f"\nTotal inserted: ${total:.2f}\n")
        return total

    def transaction(self, drink, size, price, sticker_cost):
        """
        Process payment for a drink, handle insufficient funds,
        give change, and trigger coffee preparation.
        """
        print("\n----- PAYMENT -----\n")
        total_price = price + sticker_cost
        total_paid = self.coins()
        while total_paid < total_price:
            missing = round(total_price - total_paid, 2)
            print(f"You still owe ${missing:.2f}. Please insert more coins.")
            total_paid += self.coins()
        change = round(total_paid - total_price, 2)
        print("Payment received!")
        if change > 0:
            print(f"Returning change: ${change:.2f}")
        self.make_coffee(drink, size)

    def display_menu(self):
        """Print the full drink menu with all sizes and prices."""
        print("\n----- MENU -----")
        for drink, sizes in self.choices.items():
            print(f"\n{drink}:")
            for size, info in sizes.items():
                print(f"  - {size}: ${info['Price']}")

    def take_order(self):
        """Start the order process by showing the menu and handling inputs."""
        print("\nWelcome to the FR coffee machine!\n")
        self.display_menu()
        drink = self.get_drink_choice()
        size = self.get_size_choice(drink)
        self.process_order(drink, size)

    def get_drink_choice(self):
        """Ask user to choose a drink and validate the input."""
        drinks_lower = {d.lower(): d for d in self.choices}
        while True:
            drink_input = input("\nPlease enter your drink: ").strip().lower()
            if drink_input in drinks_lower:
                return drinks_lower[drink_input]
            print("Invalid drink. Please choose again.")

    def get_size_choice(self, drink):
        """Ask user to choose a size for the selected drink."""
        sizes_lower = {s.lower(): s for s in self.choices[drink]}
        while True:
            size_input = input(f"What size for your {drink}? (Large/Medium/Small): ").strip().lower()
            if size_input in sizes_lower:
                return sizes_lower[size_input]
            print("Invalid size. Please choose again.")

    def process_order(self, drink, size):
        """
        Confirm resources, handle sticker preference,
        and start the payment flow for the drink.
        """
        if not self.check_resources(drink, size):
            print("Cannot process order due to insufficient resources.\n")
            return
        while True:
            sticker_choice = input("Would you like a sticker with your name on it? (yes/no): ").strip().lower()
            if sticker_choice in ["yes", "no"]:
                sticker_cost = 0.5 if sticker_choice == "yes" else 0
                price = self.choices[drink][size]["Price"]
                self.transaction(drink, size, price, sticker_cost)
                break
            print("Invalid input. Please type 'yes' or 'no'.")

    def add_sugar(self):
        """
        Ask how many sugar packets the user wants.
        Ensures valid amounts and updates machine resources.
        """
        while True:
            packets_input = input("How many sugar packets?(Enter 0 for none): ").strip()
            if packets_input == "":
                return 0
            try:
                packets = int(packets_input)
                if packets < 0:
                    print("Please enter a positive number.")
                    continue
                if packets > 10:
                    print(f"You can only take up to 10 sugar packets at once")
                    continue
                if packets > self.resources["Sugar Packets"]:
                    print(f"Not enough sugar! Only {self.resources['Sugar Packets']} packets left.")
                    continue
                self.resources["Sugar Packets"] -= packets
                return packets
            except ValueError:
                print("Please enter a valid number.")

    def make_coffee(self, drink, size):
        """
        Deduct required resources, simulate coffee preparation,
        handle sugar addition, and show updated resource levels.
        """
        required = self.choices[drink][size]
        for item, amount in required.items():
            if item in self.resources:
                self.resources[item] -= amount
        print("Preparing your coffee", end="", flush=True)
        for _ in range(5):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print()
        sugar = self.add_sugar()
        if sugar == 0:
            print("No sugar added.")
        else:
            print(f"{sugar} sugar packet{'s' if sugar > 1 else ''} added!")
        print(f"Your {size.lower()} {drink} is ready. Enjoy!\n")
        self.report()

    def get_positive_int(self, prompt):
        """Safely request a non-negative integer from the user."""
        while True:
            val = input(prompt).strip()
            if val == "":
                return 0
            if val.isdigit():
                return int(val)
            print("Invalid input. Enter a non-negative integer.")

    def refill_resources(self):
        """Refill one or more machine resources based on user input."""
        print("\n--- REFILLING RESOURCES ---")
        for item in self.resources:
            amount = self.get_positive_int(f"How much {item} to add? (current: {self.resources[item]}): ")
            if amount > 0:
                self.resources[item] += amount
                print(f"Added {amount} {item}. New amount: {self.resources[item]}")

    def needs_maintenance(self):
        """
        Check if any resource is too low to make at least one drink.
        Includes a sugar packet shortage check.
        """
        missing = set()
        for drink, sizes in self.choices.items():
            for size, recipe in sizes.items():
                for item, amount in recipe.items():
                    if item == "Price":
                        continue
                    if self.resources.get(item, 0) < amount:
                        missing.add(item)
        if self.resources.get("Sugar Packets", 0) <= 0:
            missing.add("Sugar Packets")              
        return list(missing) if missing else []

machine = CoffeeMachine()

while True:
    missing = machine.needs_maintenance()
    if missing:
        missing_str = ", ".join(missing).upper()
        print(f"\nMACHINE IN MAINTENANCE — OUT OF {missing_str}")
        print("Type 'refill' to restock or 'off' to shut down.")
        command = input("Command: ").lower().strip()
        if command == "refill":
            machine.refill_resources()
            continue
        elif command == "off":
            print("Shutting down...")
            break
        else:
            print("Invalid command.")
            continue

    start_machine = input("Press Enter to start or type 'off' to quit: ").lower().strip()
    if start_machine == "":
        machine.take_order()
    elif start_machine == "refill":
        machine.refill_resources()
    elif start_machine == "off":
        print("Bye! Have a nice day!")
        break
    else:
        print("Unknown command.")