import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import csv
import os
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    def scan_and_deactivate(self, person, callback=None):
        result = f"\n🧾 {self.name} is scanning {person.name}'s items at the checkout...\n"
        for item in person.items:
            scan_msg = f" - Scanning {item.name}... ✅ Tag deactivated.\n"
            result += scan_msg
            item.is_deactivated = True
            if callback:
                callback(scan_msg)
                time.sleep(0.5)
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
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
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

        # Custom fonts
        self.header_font = font.Font(size=12, weight='bold')
        self.text_font = font.Font(size=10)
        self.log_font = font.Font(size=11, family='Courier')
        self.status_font = font.Font(size=12, weight='bold')

        # Initialize counters
        self.person_counter = 0
        self.alert_counter = 0
        self.safe_scan_counter = 0

        # Available items in the store
        self.available_items = [
            Item("Milk", "RFID001"),
            Item("Bread", "RFID002"),
            Item("Cheese", "RFID003"),
            Item("Coffee", "RFID004"),
            Item("Chocolate", "RFID005")
        ]

        # Create first person
        self.new_person()
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

        # Store alert history
        self.alert_history = []

    def initialize_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Person', 'Items', 'Alert', 'Details'])

    def create_widgets(self):
        # Title and Person Info Frame
        title_frame = ttk.Frame(self.root, padding="20 20 20 10")
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = ttk.Label(
            title_frame, 
            text="Supermarket Anti-Theft System", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(side="left", padx=10)

        self.person_label = ttk.Label(
            title_frame,
            text=f"Current Customer: {self.current_person.name}",
            font=self.header_font
        )
        self.person_label.pack(side="right", padx=10)

        # Stats Frame
        stats_frame = ttk.Frame(self.root, padding="20 10")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        self.alert_label = ttk.Label(
            stats_frame,
            text="Total Alerts: 0",
            font=self.header_font,
            foreground='red'
        )
        self.alert_label.pack(side="left")

        new_person_btn = ttk.Button(
            stats_frame,
            text="New Person",
            command=self.new_person
        )
        new_person_btn.pack(side="right")

        # Analysis Frame
        analysis_frame = ttk.LabelFrame(
            self.root,
            text="Analysis Tools",
            padding="20 10 20 20"
        )
        analysis_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ttk.Button(
            analysis_frame,
            text="Show Statistics",
            command=self.show_statistics
        ).pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="Simulate Random Customers",
            command=self.simulate_random_customers
        ).pack(side="left", padx=5)

        ttk.Button(
            analysis_frame,
            text="Generate Report",
            command=self.generate_report
        ).pack(side="left", padx=5)

        # Item Selection Frame
        self.item_frame = ttk.LabelFrame(
            self.root, 
            text="Add Items to Basket", 
            padding="20 10 20 20"
        )
        self.item_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

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
        self.basket_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
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
        self.action_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # Action buttons with improved styling
        style = ttk.Style()
        style.configure('Action.TButton', font=self.text_font)
        style.configure('Alert.TButton', foreground='red')

        self.cashier_button = ttk.Button(
            self.action_frame, 
            text="Go to Cashier",
            style='Action.TButton',
            command=self.go_to_cashier,
            state=tk.DISABLED
        )
        self.cashier_button.pack(side="left", padx=10)

        self.skip_cashier_button = ttk.Button(
            self.action_frame,
            text="Skip Cashier",
            style='Alert.TButton',
            command=self.skip_cashier,
            state=tk.DISABLED
        )
        self.skip_cashier_button.pack(side="left", padx=10)

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
        self.status_frame.grid(row=6, column=0, sticky="ew", padx=20)
        
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
        self.log_frame.grid(row=7, column=0, padx=20, pady=10, sticky="nsew")
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

    def show_statistics(self):
        StatisticsWindow(self.root, self.safe_scan_counter, self.alert_counter)

    def simulate_random_customers(self):
        for _ in range(10):
            self.new_person()
            # Add 1-5 random items
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                item = random.choice(self.available_items)
                new_item = Item(item.name, item.tag_id)
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

    def generate_report(self):
        with open('summary_report.txt', 'w') as f:
            f.write("=== Supermarket Anti-Theft System Report ===\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total People Scanned: {self.person_counter}\n")
            f.write(f"Total Alerts: {self.alert_counter}\n")
            f.write(f"Total Safe Scans: {self.safe_scan_counter}\n\n")
            
            if self.alert_history:
                f.write("People Who Triggered Alerts:\n")
                for person in self.alert_history:
                    f.write(f"- {person}\n")
            else:
                f.write("No alerts were triggered during this session.\n")
        
        messagebox.showinfo("Report Generated", 
                          "Summary report has been generated as 'summary_report.txt'")

    def new_person(self):
        self.person_counter += 1
        self.current_person = Person(f"Person {self.person_counter}")
        if hasattr(self, 'person_label'):
            self.person_label.configure(text=f"Current Customer: {self.current_person.name}")
            self.clear_basket()
            self.update_status(f"New customer: {self.current_person.name}")

    def update_button_states(self):
        state = tk.NORMAL if self.current_person.items else tk.DISABLED
        self.cashier_button.configure(state=state)
        self.gate_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.skip_cashier_button.configure(state=state)

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

    def update_log_with_delay(self, message):
        self.log_text.insert("end", message)
        self.log_text.tag_add("cashier", "end-{}c".format(len(message)), "end")
        self.log_text.tag_configure("cashier", foreground="blue")
        self.log_text.see("end")
        self.root.update_idletasks()

    def skip_cashier(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        self.log_text.insert("end", f"\n⚠️ {self.current_person.name} is skipping the cashier!\n")
        self.log_text.tag_add("skip", "end-2c linestart", "end")
        self.log_text.tag_configure("skip", foreground="red")
        self.log_text.see("end")
        self.update_status("⚠️ Skipping cashier!", True)
        self.pass_through_gate()

    def go_to_cashier(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items in the basket!")
            return
        result = self.cashier.scan_and_deactivate(self.current_person, self.update_log_with_delay)
        self.update_basket_display()
        self.update_status("All items have been scanned and deactivated")

    def pass_through_gate(self):
        if not self.current_person.items:
            messagebox.showwarning("Empty Basket", "No items to scan!")
            return
        result, alert_triggered = self.gate.scan(self.current_person)
        self.log_text.insert("end", result)
        
        if alert_triggered:
            self.alert_counter += 1
            self.alert_history.append(self.current_person.name)
            self.alert_label.configure(text=f"Total Alerts: {self.alert_counter}")
            self.log_text.tag_add("alert", "end-{}c".format(len(result)), "end")
            self.log_text.tag_configure("alert", foreground="red", font=self.header_font)
            self.update_status("🚨 ALERT: Active tag detected!", True)
        else:
            self.safe_scan_counter += 1
            self.log_text.tag_add("safe", "end-{}c".format(len(result)), "end")
            self.log_text.tag_configure("safe", foreground="green")
            self.update_status("✅ All items are safe. No alert.")
        
        self.log_text.see("end")
        