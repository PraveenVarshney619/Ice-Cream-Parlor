import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog


def create_database():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        ingredients TEXT NOT NULL,
                        price REAL NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS flavor_suggestions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        suggestion TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                    )''')

    cursor.execute("DROP TABLE IF EXISTS cart")  # Added line to drop the existing cart table
    cursor.execute('''CREATE TABLE cart (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT NOT NULL,
                        price REAL NOT NULL
                    )''')  # Recreating the cart table with the correct schema

    conn.commit()
    conn.close()


def populate_sample_data():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()

    seasonal_flavors = [
        ("Vanilla Bean", "Milk, Cream, Sugar, Vanilla", 3.99),
        ("Strawberry Swirl", "Milk, Cream, Sugar, Strawberries", 4.49),
        ("Chocolate Fudge", "Milk, Cream, Sugar, Cocoa", 4.99),
        ("Mint Chocolate Chip", "Milk, Cream, Sugar, Mint, Chocolate Chips", 4.49)
    ]
    cursor.executemany("INSERT INTO seasonal_flavors (name, ingredients, price) VALUES (?, ?, ?)", seasonal_flavors)

    ingredients = [
        ("Milk", 100),
        ("Cream", 50),
        ("Sugar", 200),
        ("Vanilla", 30),
        ("Strawberries", 25),
        ("Cocoa", 20),
        ("Mint", 15),
        ("Chocolate Chips", 40)
    ]
    cursor.executemany("INSERT INTO ingredients (name, quantity) VALUES (?, ?)", ingredients)

    flavor_suggestions = [
        ("Blueberry Cheesecake",),
        ("Salted Caramel",),
        ("Pistachio",),
        ("Raspberry Ripple",)
    ]
    cursor.executemany("INSERT INTO flavor_suggestions (suggestion) VALUES (?)", flavor_suggestions)

    allergens = [
        ("Milk",),
        ("Nuts",),
        ("Gluten",),
        ("Soy",),
        ("Eggs",)
    ]
    cursor.executemany("INSERT INTO allergens (name) VALUES (?)", allergens)

    conn.commit()
    conn.close()


class IceCreamParlorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ice Cream Parlor Cafe")

        self.conn = sqlite3.connect('ice_cream_parlor.db')
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Seasonal Flavors Section
        self.flavors_frame = tk.LabelFrame(self.main_frame, text="Seasonal Flavors", padx=10, pady=10)
        self.flavors_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.flavors_listbox = tk.Listbox(self.flavors_frame, height=10, width=50)
        self.flavors_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.search_entry = tk.Entry(self.flavors_frame, width=30)
        self.search_entry.grid(row=1, column=0, padx=5, pady=5)

        self.search_button = tk.Button(self.flavors_frame, text="Search", command=self.search_flavors)
        self.search_button.grid(row=1, column=1, padx=5, pady=5)

        self.add_flavor_button = tk.Button(self.flavors_frame, text="Add Flavor", command=self.add_flavor)
        self.add_flavor_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Cart Section
        self.cart_frame = tk.LabelFrame(self.main_frame, text="My Cart", padx=10, pady=10)
        self.cart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.cart_listbox = tk.Listbox(self.cart_frame, height=10, width=50)
        self.cart_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_to_cart_button = tk.Button(self.cart_frame, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=1, column=0, padx=5, pady=5)

        self.delete_from_cart_button = tk.Button(self.cart_frame, text="Delete from Cart",
                                                 command=self.delete_from_cart)
        self.delete_from_cart_button.grid(row=1, column=1, padx=5, pady=5)

        self.total_label = tk.Label(self.cart_frame, text="Total: $0.00 (0 items)")
        self.total_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Allergen Section
        self.allergen_frame = tk.LabelFrame(self.main_frame, text="Allergens", padx=10, pady=10)
        self.allergen_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.allergen_listbox = tk.Listbox(self.allergen_frame, height=10, width=50)
        self.allergen_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.add_allergen_button = tk.Button(self.allergen_frame, text="Add Allergen", command=self.add_allergen)
        self.add_allergen_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Ingredient Inventory Section
        self.inventory_frame = tk.LabelFrame(self.main_frame, text="Ingredient Inventory", padx=10, pady=10)
        self.inventory_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.inventory_listbox = tk.Listbox(self.inventory_frame, height=10, width=50)
        self.inventory_listbox.grid(row=0, column=0, padx=5, pady=5)

        # Customer Flavor Suggestions Section
        self.suggestions_frame = tk.LabelFrame(self.main_frame, text="Flavor Suggestions", padx=10, pady=10)
        self.suggestions_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.suggestions_listbox = tk.Listbox(self.suggestions_frame, height=10, width=100)
        self.suggestions_listbox.grid(row=0, column=0, padx=5, pady=5)

        self.load_flavors()
        self.load_cart()
        self.load_allergens()
        self.load_inventory()
        self.load_suggestions()

    def load_flavors(self):
        self.flavors_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name, price FROM seasonal_flavors")
        for row in self.cursor.fetchall():
            self.flavors_listbox.insert(tk.END, f"{row[0]} - ${row[1]:.2f}")

    def search_flavors(self):
        search_term = self.search_entry.get()
        self.flavors_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name, price FROM seasonal_flavors WHERE name LIKE ?", ('%' + search_term + '%',))
        for row in self.cursor.fetchall():
            self.flavors_listbox.insert(tk.END, f"{row[0]} - ${row[1]:.2f}")

    def add_flavor(self):
        flavor_name = simpledialog.askstring("Input", "Enter the flavor name:")
        ingredients = simpledialog.askstring("Input", "Enter the ingredients:")
        price = simpledialog.askfloat("Input", "Enter the price:")
        if flavor_name and ingredients and price is not None:
            self.cursor.execute("INSERT INTO seasonal_flavors (name, ingredients, price) VALUES (?, ?, ?)",
                                (flavor_name, ingredients, price))
            self.conn.commit()
            self.load_flavors()
        else:
            messagebox.showwarning("Input Error", "Please enter flavor name, ingredients, and price.")

    def add_to_cart(self):
        selected_flavor = self.flavors_listbox.get(tk.ACTIVE)
        if selected_flavor:
            flavor_name = selected_flavor.split(" - $")[0]
            price = float(selected_flavor.split(" - $")[1])
            self.cursor.execute("INSERT INTO cart (product_name, price) VALUES (?, ?)", (flavor_name, price))
            self.conn.commit()
            self.load_cart()
        else:
            messagebox.showwarning("Selection Error", "Please select a flavor to add to the cart.")

    def delete_from_cart(self):
        selected_item = self.cart_listbox.get(tk.ACTIVE)
        if selected_item:
            self.cursor.execute("DELETE FROM cart WHERE product_name = ? LIMIT 1", (selected_item,))
            self.conn.commit()
            self.load_cart()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete from the cart.")

    def load_cart(self):
        self.cart_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT product_name, price FROM cart")
        total_price = 0
        total_items = 0
        for row in self.cursor.fetchall():
            self.cart_listbox.insert(tk.END, row[0])
            total_price += row[1]
            total_items += 1
        self.total_label.config(text=f"Total: ${total_price:.2f} ({total_items} items)")

    def load_allergens(self):
        self.allergen_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name FROM allergens")
        for row in self.cursor.fetchall():
            self.allergen_listbox.insert(tk.END, row[0])

    def add_allergen(self):
        allergen_name = simpledialog.askstring("Input", "Enter the allergen name:")
        if allergen_name:
            self.cursor.execute("INSERT INTO allergens (name) VALUES (?)", (allergen_name,))
            self.conn.commit()
            self.load_allergens()
        else:
            messagebox.showwarning("Input Error", "Please enter an allergen name.")

    def load_inventory(self):
        self.inventory_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT name, quantity FROM ingredients")
        for row in self.cursor.fetchall():
            self.inventory_listbox.insert(tk.END, f"{row[0]}: {row[1]} units")

    def load_suggestions(self):
        self.suggestions_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT suggestion FROM flavor_suggestions")
        for row in self.cursor.fetchall():
            self.suggestions_listbox.insert(tk.END, row[0])


if __name__ == "__main__":
    create_database()
    populate_sample_data()
    root = tk.Tk()
    app = IceCreamParlorApp(root)
    root.mainloop()
