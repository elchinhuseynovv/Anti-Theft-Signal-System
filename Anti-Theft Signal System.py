import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv

class Item:
    def __init__(self, name, tag_id, is_deactivated=False):
        self.name = name
        self.tag_id = tag_id
        self.is_deactivated = is_deactivated

    def __str__(self):
        status = "Deactivated" if self.is_deactivated else "Active"
        return f"{self.name} (Tag: {self.tag_id}, {status})"


class Person:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __str__(self):
        return f"{self.name} is carrying {len(self.items)} item(s)."


class Cashier:
    def __init__(self, name):
        self.name = name

    def scan_and_deactivate(self, person):
        result = f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...\n"
        for item in person.items:
            result += f" - Scanning {item.name}... ✅ Tag deactivated.\n"
            item.is_deactivated = True
        return result


class Gate:
    def __init__(self):
        pass

    def scan(self, person):
        result = f"\n🚪 Scanning {person.name} at the exit gate...\n"
        alert_triggered = False
        for item in person.items:
            result += f" - Checking item: {item}\n"
            if not item.is_deactivated:
                result += "   🔴 ALERT: Active tag detected! Possible theft!\n"
                alert_triggered = True
        if not alert_triggered:
            result += "✅ All items are safe. No alert.\n"
        return result, alert_triggered


class AntiTheftGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Anti-Theft System")
        self.root.geometry("800x600")

        # Available items in the store
        self.available_items = [
            Item("Milk", "RFID001"),
            Item("Bread", "RFID002"),
            Item("Cheese", "RFID003"),
            Item("Coffee", "RFID004"),
            Item("Chocolate", "RFID005")
        ]

        # Create current person
        self.current_person = Person("Customer")
        self.cashier = Cashier("Sarah")
        self.gate = Gate()

        self.create_widgets()
        self.log_file = "alerts.csv"
        self.initialize_log_file()

    def initialize_log_file(self):
        with open(self.log_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Event', 'Alert'])

    def create_widgets(self):
        # Create frames
        self.item_frame = ttk.LabelFrame(self.root, text="Item Selection", padding=10)
        self.item_frame.pack(fill="x", padx=10, pady=5)

        self.action_frame = ttk.LabelFrame(self.root, text="Actions", padding=10)
        self.action_frame.pack(fill="x", padx=10, pady=5)

        self.log_frame = ttk.LabelFrame(self.root, text="System Log", padding=10)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Item selection
        self.item_var = tk.StringVar()
        item_names = [item.name for item in self.available_items]
        self.item_dropdown = ttk.Combobox(self.item_frame, textvariable=self.item_var, values=item_names)
        self.item_dropdown.pack(side="left", padx=5)
        
        self.add_button = ttk.Button(self.item_frame, text="Add to Basket", command=self.add_item)
        self.add_button.pack(side="left", padx=5)

        # Action buttons
        self.cashier_button = ttk.Button(self.action_frame, text="Go to Cashier", command=self.go_to_cashier)
        self.cashier_button.pack(side="left", padx=5)

        self.gate_button = ttk.Button(self.action_frame, text="Pass Through Gate", command=self.pass_through_gate)
        self.gate_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(self.action_frame, text="Clear Basket", command=self.clear_basket)
        self.clear_button.pack(side="left", padx=5)

        # Log display
        self.log_text = tk.Text(self.log_frame, height=20, width=70)
        self.log_text.pack(fill="both", expand=True)

    def add_item(self):
        selected_item_name = self.item_var.get()
        if selected_item_name:
            # Create a new instance of the selected item
            for item in self.available_items:
                if item.name == selected_item_name:
                    new_item = Item(item.name, item.tag_id)
                    self.current_person.add_item(new_item)
                    self.log_text.insert("end", f"Added {new_item.name} to basket\n")
                    self.log_text.see("end")
                    break

    def go_to_cashier(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        result = self.cashier.scan_and_deactivate(self.current_person)
        self.log_text.insert("end", result)
        self.log_text.see("end")

    def pass_through_gate(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items to scan!")
            return
        result, alert_triggered = self.gate.scan(self.current_person)
        self.log_text.insert("end", result)
        self.log_text.see("end")
        
        # Log to CSV
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gate Scan",
                "Alert Triggered" if alert_triggered else "No Alert"
            ])

    def clear_basket(self):
        self.current_person.items = []
        self.log_text.insert("end", "Basket cleared\n")
        self.log_text.see("end")


if __name__ == "__main__":
    root = tk.Tk()
    app = AntiTheftGUI(root)
    root.mainloop()