import json

class Item:
    id = 0  #keeps track of item IDs

    def __init__(self, name, color, size, price):
        Item.id += 1
        self.ID = Item.id
        self.name = name
        self.color = color
        self.size = size
        self.price = price

    def get_details(self):
        return f"ID: {self.ID}, Name: {self.name}, Color: {self.color}, Size: {self.size}, Price: ${self.price:.2f}"

    def to_dict(self):
        """Convert item to dictionary for JSON serialization"""
        return {
            "ID": self.ID,
            "name": self.name,
            "color": self.color,
            "size": self.size,
            "price": self.price
        }


class Inventory:
    def __init__(self):
        self.items = {}
        self.load_inventory()  #trys to load inventory from json file if there is one

    def add_item(self, item):
        if item.ID in self.items:
            print(f"Item with ID {item.ID} already exists.")
        else:
            self.items[item.ID] = item
            print(f"Item '{item.name}' added to inventory.")

    def remove_item(self, item_id):
        if item_id in self.items:
            removed_item = self.items.pop(item_id)
            print(f"Item '{removed_item.name}' removed from inventory.")
        else:
            print(f"Item with ID {item_id} not found in inventory.")

    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            for item in self.items.values():
                print(item.get_details())

    def check_stock(self):
        print(f"Total items in stock: {len(self.items)}")

    def load_inventory(self):
        #loads inventory from json file if it exists
        try:
            with open('inventory.json', 'r') as file:
                data = json.load(file)
                for item_data in data:
                    item = Item(
                        item_data['name'],
                        item_data['color'],
                        item_data['size'],
                        item_data['price']
                    )
                    self.items[item.ID] = item
            print("Inventory loaded from 'inventory.json'.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("No previous inventory found. Starting with an empty inventory.")

    def save_inventory(self):
        """Save the inventory to the JSON file"""
        inventory_list = [item.to_dict() for item in self.items.values()]
        with open('inventory.json', 'w') as file:
            json.dump(inventory_list, file, indent=4)
        print("Inventory saved to 'inventory.json'.")


class User:

    def __init__(self):
        self.name = ""
        self.role = ""

    def login(self):
        self.name = input("Enter your Username: ")
        while True:
            self.role = input("Enter your Role (Admin/Manager): ").upper()
            if self.role in ["ADMIN", "MANAGER"]:
                print("Login Successful!")
                break
            else:
                print("Invalid role. Please enter 'Admin' or 'Manager'.")

    def get_permissions(self):
        permissions = {
            "ADMIN": "Admin, your permissions are: Add, Remove, Update, List, Check Stock, Check Details",
            "MANAGER": "Manager, your permissions are: List, Check Stock, Check Details"
        }
        return permissions.get(self.role, "No permissions found.")

    def perform_inventory_actions(self, inventory):
        while True:
            if self.role == "ADMIN":
                print("\n1. Add Item\n2. Remove Item\n3. List Items\n4. Check Stock\n5. Logout or type 'logout'")
                choice = input("Choose an action: ").strip().lower()
                if choice == "1":
                    self.add_item(inventory)
                elif choice == "2":
                    self.remove_item(inventory)
                elif choice == "3":
                    inventory.list_items()
                elif choice == "4":
                    inventory.check_stock()
                elif choice == "5" or choice == "logout":  # Log out
                    print("Logging out...")
                    inventory.save_inventory()  # Save inventory before logout
                    return False
                else:
                    print("Invalid choice. Please try again.")
            elif self.role == "MANAGER":
                print("\n1. List Items\n2. Check Stock\n3. Check Item Details\n4. Logout or type 'logout'")
                choice = input("Choose an action: ").strip().lower()
                if choice == "1":
                    inventory.list_items()
                elif choice == "2":
                    inventory.check_stock()
                elif choice == "3":
                    self.check_item_details(inventory)
                elif choice == "4" or choice == "logout":  # Log out
                    print("Logging out...")
                    inventory.save_inventory()  # Save inventory before logout
                    return False
                else:
                    print("Invalid choice. Please try again.")

    def add_item(self, inventory):
        name = input("Enter item name: ")
        color = input("Enter item color: ")
        size = input("Enter item size: ")
        try:
            price = float(input("Enter item price: "))
            if price <= 0:
                print("Price must be greater than zero.")
                return
            new_item = Item(name, color, size, price)
            inventory.add_item(new_item)
        except ValueError:
            print("Invalid price entered. Please enter a valid number.")

    def remove_item(self, inventory):
        try:
            item_id = int(input("Enter item ID to remove: "))
            inventory.remove_item(item_id)
        except ValueError:
            print("Invalid ID. Please enter a valid number.")

    def check_item_details(self, inventory):
        try:
            item_id = int(input("Enter item ID to check details: "))
            if item_id in inventory.items:
                print(inventory.items[item_id].get_details())
            else:
                print(f"Item with ID {item_id} not found.")
        except ValueError:
            print("Invalid ID. Please enter a valid number.")


class Main:

    def __init__(self):
        self.inventory = Inventory()

    def start(self):
        logged_out = False  #will indicate if user has logged out
        while not logged_out:
            print("\nWELCOME to the Toy Shop Employee portal, please login")
            user = User()
            user.login()
            print(user.get_permissions())
            logged_out = not user.perform_inventory_actions(self.inventory)  #on logout logged_out becomes True

        print("Thank you for using the Toy Shop portal!")


# Starting the main program
if __name__ == "__main__":
    main_program = Main()
    main_program.start()
