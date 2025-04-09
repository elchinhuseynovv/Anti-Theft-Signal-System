import tkinter as tk
from tkinter import ttk, messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from models import Item, Person, Cashier, Gate
from logger import SystemLogger

class StatisticsWindow:
    def __init__(self, parent, safe_scans, alert_scans):
        self.window = tk.Toplevel(parent)
        self.window.title("Scan Statistics")
        self.window.geometry("600x400")
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Safe Scans', 'Alert Scans']
        sizes = [safe_scans, alert_scans]
        colors = ['#2ecc71', '#e74c3c']
        
        if sum(sizes) > 0:  # Only create pie chart if there's data
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        else:
            ax.text(0.5, 0.5, 'No scan data available', 
                   horizontalalignment='center',
                   verticalalignment='center')
            ax.axis('off')
        
        # Embed plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


class AntiTheftGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Anti-Theft System")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        # Initialize fonts
        self.header_font = font.Font(size=12, weight='bold')
        self.text_font = font.Font(size=10)
        self.log_font = font.Font(size=11, family='Courier')
        self.status_font = font.Font(size=12, weight='bold')

        # Initialize counters and system components
        self.person_counter = 0
        self.alert_counter = 0
        self.safe_scan_counter = 0
        self.alert_history = []
        
        # Initialize logger
        self.logger = SystemLogger()

        # Available items in the store with prices
        self.available_items = [
            Item("Milk", "RFID001", price=3.99, category="Dairy"),
            Item("Bread", "RFID002", price=2.49, category="Bakery"),
            Item("Cheese", "RFID003", price=4.99, category="Dairy"),
            Item("Coffee", "RFID004", price=7.99, category="Beverages"),
            Item("Chocolate", "RFID005", price=1.99, category="Snacks")
        ]

        # Create first person and system components
        self.new_person()
        self.cashier = Cashier("Sarah")
        self.gate = Gate()

        self.create_widgets()
        self.update_button_states()

    def simulate_random_customers(self):
        """Simulate multiple customers with random behaviors."""
        try:
            for _ in range(10):
                self.new_person()
                # Add 1-5 random items
                num_items = random.randint(1, 5)
                for _ in range(num_items):
                    item = random.choice(self.available_items)
                    new_item = Item(item.name, item.tag_id, price=item.price, category=item.category)
                    self.current_person.add_item(new_item)
                    self.update_basket_display()
                    self.update_button_states()
                    self.root.update_idletasks()
                    time.sleep(0.2)
                
                # 30% chance to skip cashier
                if random.random() < 0.3:
                    self.skip_cashier()
                else:
                    self.go_to_cashier()
                
                self.pass_through_gate()
                time.sleep(0.5)
        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}")

    def create_widgets(self):
        """Create all GUI widgets."""
        # [Previous widget creation code remains the same]
        # Include all the widget creation code from the original file here
        pass  # Remove this line when adding the widget creation code

    def update_button_states(self):
        """Update the state of all buttons based on current conditions."""
        state = tk.NORMAL if self.current_person.items else tk.DISABLED
        self.cashier_button.configure(state=state)
        self.gate_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.skip_cashier_button.configure(state=state)

    def update_basket_display(self):
        """Update the basket display with current items."""
        self.basket_display.config(state=tk.NORMAL)
        self.basket_display.delete(1.0, tk.END)
        if self.current_person.items:
            total = 0.0
            for item in self.current_person.items:
                status = "✅ Deactivated" if item.is_deactivated else "🔴 Active"
                self.basket_display.insert(tk.END, 
                    f"• {item.name} (${item.price:.2f}) - {status}\n")
                total += item.price
            self.basket_display.insert(tk.END, f"\nTotal: ${total:.2f}")
        else:
            self.basket_display.insert(tk.END, "Basket is empty")
        self.basket_display.config(state=tk.DISABLED)

    def update_status(self, message, is_alert=False):
        """Update the status message."""
        color = '#ff0000' if is_alert else '#008000'
        self.status_label.configure(text=message, foreground=color)

    def new_person(self):
        """Create a new person."""
        self.person_counter += 1
        self.current_person = Person(f"Person {self.person_counter}")
        if hasattr(self, 'person_label'):
            self.person_label.configure(text=f"Current Customer: {self.current_person.name}")
            self.clear_basket()
            self.update_status(f"New customer: {self.current_person.name}")

    def add_item(self):
        """Add an item to the current person's basket."""
        selected_item_name = self.item_var.get()
        if selected_item_name:
            for item in self.available_items:
                if item.name == selected_item_name:
                    new_item = Item(item.name, item.tag_id, 
                                  price=item.price, category=item.category)
                    self.current_person.add_item(new_item)
                    self.log_text.insert("end", 
                        f"➕ Added {new_item.name} (${new_item.price:.2f}) to basket\n")
                    self.log_text.see("end")
                    self.update_basket_display()
                    self.update_button_states()
                    self.update_status(f"Added {new_item.name} to basket")
                    break
