import tkinter as tk
from tkinter import ttk, messagebox, font
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
        self.root.geometry("1000x900")  # Increased height for new elements
        self.root.configure(bg='#f0f0f0')

        # Custom fonts
        self.header_font = font.Font(size=12, weight='bold')
        self.text_font = font.Font(size=10)
        self.log_font = font.Font(size=11, family='Courier')
        self.status_font = font.Font(size=12, weight='bold')

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

        # Configure grid weights
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Initialize button states
        self.update_button_states()

    def initialize_log_file(self):
        with open(self.log_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Event', 'Alert'])

    def create_widgets(self):
        # Title Frame
        title_frame = ttk.Frame(self.root, padding="20 20 20 10")
        title_frame.grid(row=0, column=0, sticky="ew")
        title_label = ttk.Label(
            title_frame, 
            text="Supermarket Anti-Theft System", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack()

        # Item Selection Frame
        self.item_frame = ttk.LabelFrame(
            self.root, 
            text="Person's Basket", 
            padding="20 10 20 20"
        )
        self.item_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Configure item frame grid
        self.item_frame.columnconfigure(1, weight=1)
        
        # Item selection widgets
        ttk.Label(
            self.item_frame, 
            text="Select Item:", 
            font=self.header_font
        ).grid(row=0, column=0, padx=5, pady=5)
        
        self.item_var = tk.StringVar()
        item_names = [item.name for item in self.available_items]
        self.item_dropdown = ttk.Combobox(
            self.item_frame, 
            textvariable=self.item_var, 
            values=item_names,
            width=30
        )
        self.item_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.add_button = ttk.Button(
            self.item_frame, 
            text="Add to Basket",
            command=self.add_item
        )
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        # Current Basket Frame
        self.basket_frame = ttk.LabelFrame(
            self.root,
            text="Current Basket",
            padding="20 10 20 20"
        )
        self.basket_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Basket display
        self.basket_display = tk.Text(
            self.basket_frame,
            height=5,
            width=70,
            font=self.text_font,
            wrap=tk.WORD,
            bg='#ffffff',
            fg='#000000'
        )
        self.basket_display.pack(fill=tk.BOTH, expand=True)
        self.basket_display.config(state=tk.DISABLED)

        # Actions Frame
        self.action_frame = ttk.LabelFrame(
            self.root, 
            text="Actions", 
            padding="20 10 20 20"
        )
        self.action_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Action buttons with improved styling
        style = ttk.Style()
        style.configure('Action.TButton', font=self.text_font)

        self.cashier_button = ttk.Button(
            self.action_frame, 
            text="Go to Cashier",
            style='Action.TButton',
            command=self.go_to_cashier,
            state=tk.DISABLED
        )
        self.cashier_button.pack(side="left", padx=10)

        self.gate_button = ttk.Button(
            self.action_frame, 
            text="Pass Through Gate",
            style='Action.TButton',
            command=self.pass_through_gate,
            state=tk.DISABLED
        )
        self.gate_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(
            self.action_frame, 
            text="Clear Basket",
            style='Action.TButton',
            command=self.clear_basket,
            state=tk.DISABLED
        )
        self.clear_button.pack(side="left", padx=10)

        # Status Label Frame
        self.status_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.status_frame.grid(row=4, column=0, sticky="ew", padx=20)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to scan items",
            font=self.status_font,
            foreground='#666666'
        )
        self.status_label.pack()

        # System Log Frame
        self.log_frame = ttk.LabelFrame(
            self.root, 
            text="System Log", 
            padding="20 10 20 20"
        )
        self.log_frame.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        # Log display with custom font and colors
        self.log_text = tk.Text(
            self.log_frame,
            height=15,
            width=70,
            font=self.log_font,
            wrap=tk.WORD,
            bg='#ffffff',
            fg='#000000'
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # Add scrollbar to log
        scrollbar = ttk.Scrollbar(
            self.log_frame,
            orient="vertical",
            command=self.log_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def update_button_states(self):
        state = tk.NORMAL if self.current_person.items else tk.DISABLED
        self.cashier_button.configure(state=state)
        self.gate_button.configure(state=state)
        self.clear_button.configure(state=state)

    def update_basket_display(self):
        self.basket_display.config(state=tk.NORMAL)
        self.basket_display.delete(1.0, tk.END)
        if self.current_person.items:
            for item in self.current_person.items:
                status = "✅ Deactivated" if item.is_deactivated else "🔴 Active"
                self.basket_display.insert(tk.END, f"• {item.name} ({status})\n")
        else:
            self.basket_display.insert(tk.END, "Basket is empty")
        self.basket_display.config(state=tk.DISABLED)

    def update_status(self, message, is_alert=False):
        color = '#ff0000' if is_alert else '#008000'
        self.status_label.configure(text=message, foreground=color)

    def add_item(self):
        selected_item_name = self.item_var.get()
        if selected_item_name:
            # Create a new instance of the selected item
            for item in self.available_items:
                if item.name == selected_item_name:
                    new_item = Item(item.name, item.tag_id)
                    self.current_person.add_item(new_item)
                    self.log_text.insert("end", f"➕ Added {new_item.name} to basket\n")
                    self.log_text.tag_add("success", "end-2c linestart", "end")
                    self.log_text.tag_configure("success", foreground="green")
                    self.log_text.see("end")
                    self.update_basket_display()
                    self.update_button_states()
                    self.update_status(f"Added {new_item.name} to basket")
                    break

    def go_to_cashier(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        result = self.cashier.scan_and_deactivate(self.current_person)
        self.log_text.insert("end", result)
        self.log_text.tag_add("cashier", "end-{}c".format(len(result)), "end")
        self.log_text.tag_configure("cashier", foreground="blue")
        self.log_text.see("end")
        self.update_basket_display()
        self.update_status("All items have been scanned and deactivated")

    def pass_through_gate(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items to scan!")
            return
        result, alert_triggered = self.gate.scan(self.current_person)
        self.log_text.insert("end", result)
        
        # Apply color tags based on alert status
        if alert_triggered:
            self.log_text.tag_add("alert", "end-{}c".format(len(result)), "end")
            self.log_text.tag_configure("alert", foreground="red", font=self.header_font)
            self.update_status("🚨 ALERT: Active tag detected!", True)
        else:
            self.log_text.tag_add("safe", "end-{}c".format(len(result)), "end")
            self.log_text.tag_configure("safe", foreground="green")
            self.update_status("✅ All items are safe. No alert.")
        
        self.log_text.see("end")
        